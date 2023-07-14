from pathlib import Path
from typing import IO, Tuple, Union
from .crc import CRC32

# ! FP Functions
def initfp(fp: Union[str, Path, IO[bytes]]) -> Tuple[str, IO[bytes]]: ...
def iocopy(from_io: IO[bytes], to_io: IO[bytes], size: int, buffer_size: int=8192) -> CRC32: ...