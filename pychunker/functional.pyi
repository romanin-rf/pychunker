import sys
from pathlib import Path
from io import BytesIO, BufferedRandom, DEFAULT_BUFFER_SIZE
# > Typing
from typing import Literal, Iterable, Tuple, Union, Optional, IO, overload
# > Local Imports
from .types import T, CFMode
from .crc import CRC32

# ! IO Methods
@overload
def initfp(fp: Union[str, Path], mode: CFMode) -> Tuple[str, BufferedRandom]: ...
@overload
def initfp(fp: BufferedRandom, mode: CFMode) -> Tuple[str, BufferedRandom]: ...
@overload
def initfp(fp: BytesIO, mode: CFMode) -> Tuple[None, BytesIO]: ...
@overload
def initfp(fp: IO[bytes], mode: CFMode) -> Tuple[Optional[str], IO[bytes]]: ...

def iocopy(
    from_io: IO[bytes],
    to_io: IO[bytes],
    size: int,
    buffer_size: int=DEFAULT_BUFFER_SIZE,
    byteorder=sys.byteorder
) -> CRC32: ...

# ! Has Methods
def hasitem(value: Iterable[T], items: Iterable[T]) -> bool: ...
def hasitems(value: Iterable[T], items: Iterable[T]) -> bool: ...

@overload
def is_cfmode(value: CFMode) -> Literal[True]: ...
@overload
def is_cfmode(value: str) -> Literal[False]: ...

# ! Formatting Methods
def formater(**kwargs: object) -> str: ...