import binascii
from collections.abc import Callable
import logging
from concurrent.futures import FIRST_EXCEPTION, Future, ThreadPoolExecutor, wait
from dataclasses import dataclass, field
from queue import Queue
from threading import Lock
from typing import IO

from vcf_generator_lite.models.contact import Contact, PhoneNotFoundError, parse_contact

_logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class InvalidLine:
    row_position: int
    content: str
    exception: BaseException


@dataclass
class VCardGeneratorState:
    total: int = 0
    processed: int = 0
    progress: float = 0
    invalid_lines: list[InvalidLine] = field(default_factory=list)
    running: bool = False


@dataclass(frozen=True)
class GenerateResult:
    invalid_lines: list[InvalidLine]
    exception: BaseException | None = None


def utf8_to_qp(text: str) -> str:
    return binascii.b2a_qp(text.encode("utf-8")).decode("utf-8")


def serialize_to_vcard(contact: Contact):
    items: list[str | None] = [
        "BEGIN:VCARD",
        "VERSION:2.1",
        f"FN;CHARSET=UTF-8;ENCODING=QUOTED-PRINTABLE:{utf8_to_qp(contact.name)}" if contact.name else None,
        f"TEL;CELL:{contact.phone}",
        f"NOTE;CHARSET=UTF-8;ENCODING=QUOTED-PRINTABLE:{utf8_to_qp(contact.note)}" if contact.note else None,
        "END:VCARD",
    ]
    filtered_items = (item for item in items if item is not None)
    return "\n".join(filtered_items)


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

        exception: BaseException | None = None
        for future in done:
            exception = future.exception()
            if exception:
                break
        return GenerateResult(
            invalid_lines=self._state.invalid_lines,
            exception=exception,
        )

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
            except PhoneNotFoundError as e:
                self._finish_item()
                _logger.warning(f"Phone not found at line {position}: {e}")
                with self._lock:
                    self._state.invalid_lines.append(InvalidLine(row_position=position, content=line, exception=e))
            except Exception as e:
                self._finish_item()
                _logger.warning(f"Unexpected parsing error at line {position}", exc_info=e)
                with self._lock:
                    self._state.invalid_lines.append(InvalidLine(row_position=position, content=line, exception=e))

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
