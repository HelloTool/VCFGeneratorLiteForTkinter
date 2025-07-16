import math
import shutil
import subprocess
import sys


def get_bits() -> int:
    return int(math.log(sys.maxsize + 1, 2) + 1)


def require_64_bits() -> None:
    if get_bits() != 64:
        print(f"Python must be 64-bit, but it is {get_bits()}-bit. Current Python Information:")
        if (pdm_path := shutil.which("pdm")) is not None:
            subprocess.run([pdm_path, "run", "python", "-VV"])
            subprocess.run([pdm_path, "run", "python", "-v", "-c", "exit()"])
        raise RuntimeError(f"64-bit Python is required, but {get_bits()}-bit Python is found.")
