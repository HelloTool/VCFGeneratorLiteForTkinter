import binascii
from collections.abc import Callable
import logging
from concurrent.futures import FIRST_EXCEPTION, Future, ThreadPoolExecutor, wait
from dataclasses import dataclass, field
from queue import Queue
from threading import Lock
from typing import IO

from vcf_generator_lite.models.contact import Contact, parse_contact

_logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class InvalidLine:
    row_position: int
    content: str
    reason: str


@dataclass
class VCardGeneratorState:
    total: int = 0
    processed: int = 0
    progress: float = 0
    invalid_lines: list[InvalidLine] = field(default_factory=list)
    exceptions: list[BaseException] = field(default_factory=list)
    running: bool = False


@dataclass(frozen=True)
class GenerateResult:
    invalid_lines: list[InvalidLine]
    exceptions: list[BaseException]


def utf8_to_qp(text: str) -> str:
    return binascii.b2a_qp(text.encode("utf-8")).decode("utf-8")


def serialize_to_vcard(contact: Contact):
    items: list[str] = [
        "BEGIN:VCARD",
        "VERSION:2.1",
        f"FN;CHARSET=UTF-8;ENCODING=QUOTED-PRINTABLE:{utf8_to_qp(contact.name)}",
        f"TEL;CELL:{contact.phone}",
    ]
    if contact.note:
        items.append(f"NOTE;CHARSET=UTF-8;ENCODING=QUOTED-PRINTABLE:{utf8_to_qp(contact.note)}")
    items.append("END:VCARD")
    return "\n".join(items)


class VCFGeneratorTask:
    def __init__(
        self,
        executor: ThreadPoolExecutor,
        progress_listener: Callable[[float, bool], None] | None,
        input_text: str,
        output_io: IO[str],
    ):
        self._executor = executor
        self._progress_listener = progress_listener
        self._input_text = input_text
        self._output_io = output_io
        self._state = VCardGeneratorState()
        self._lock = Lock()
        self._write_queue: Queue[str | None] = Queue()

    def start(self) -> Future[GenerateResult]:
        future = self._executor.submit(self._process)
        return future

    def _process(self) -> GenerateResult:
        self._state.running = True
        with ThreadPoolExecutor(max_workers=2, thread_name_prefix="VCFGenerator") as pipeline_executor:
            parse_future = pipeline_executor.submit(self._parse_input)
            write_future = pipeline_executor.submit(self._write_output)
            done, _ = wait([parse_future, write_future], return_when=FIRST_EXCEPTION)
        self._state.running = False
        # 收集异常
        for future in done:
            if exception := future.exception():
                with self._lock:
                    self._state.exceptions.append(exception)
        return GenerateResult(invalid_lines=self._state.invalid_lines, exceptions=self._state.exceptions)

    def _parse_input(self) -> None:
        lines = [line.strip() for line in self._input_text.split("\n")]
        self._state.total = len(lines)
        self._notify_progress()
        for position, line in enumerate(lines):
            if not self._state.running:
                break
            if line.strip() == "":
                self._finish_item()
                continue
            try:
                contact = parse_contact(line)
                vcard = serialize_to_vcard(contact)
                self._write_queue.put(vcard)
            except ValueError as e:
                self._finish_item()
                _logger.warning(f"Invalid contact data at line {position}: {e}")
                with self._lock:
                    self._state.invalid_lines.append(InvalidLine(position, line, str(e)))
            except Exception as e:
                self._finish_item()
                _logger.exception(f"Unexpected parsing error at line {position}", exc_info=e)
                with self._lock:
                    self._state.exceptions.append(e)

        self._write_queue.put(None)  # 结束信号

    def _write_output(self):
        while self._state.running and ((item := self._write_queue.get()) is not None):
            try:
                self._output_io.write(item)
                self._output_io.write("\n\n")
            finally:
                self._write_queue.task_done()
                self._finish_item()

    def _notify_progress(self):
        if self._progress_listener is None:
            return
        self._progress_listener(self._state.progress, self._state.total > 0)

    def _increment_progress(self, increment: int = 1):
        if self._state.total == 0:
            return
        with self._lock:
            self._state.processed += increment
            new_progress = round(min(self._state.processed / self._state.total, 1.0), 1)
            if self._state.progress != new_progress:
                self._state.progress = new_progress
                self._notify_progress()

    def _finish_item(self):
        self._increment_progress()
