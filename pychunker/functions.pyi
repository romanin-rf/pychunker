from pathlib import Path
from io import DEFAULT_BUFFER_SIZE
from typing import IO, Tuple, Literal, Optional, Union
from .crc import CRC32
from .types import BinaryModeUpdating

# ! FP Functions
def initfp(
    fp: Union[str, Path, IO[bytes]],
    needed_mode: Literal['r', 'w', 'a']='a'
) -> Tuple[Optional[str], IO[bytes]]:
    """Initializing IO to work with chunks.
    
    Args:
        fp (Union[str, Path, IO[bytes]]): IO of a chunk file.
    
    Returns:
        Tuple[Optional[str], IO[bytes]]: Data for working with chunks.
    """
    ...

def iocopy(
    from_io: IO[bytes],
    to_io: IO[bytes],
    size: int,
    buffer_size: int=DEFAULT_BUFFER_SIZE
) -> CRC32:
    """Copying IO with additional checksum calculation.
    
    Args:
        from_io (IO[bytes]): The IO from which it will be copied.
        to_io (IO[bytes]): The IO to which it will be copied.
        size (int): The amount that will be copied.
        buffer_size (int, optional): The size of the temporary data. Defaults to 8192.
    
    Returns:
        CRC32: The checksum.
    """
    ...

def formater(**kwargs: object) -> str:
    """Rationalization of values.
    
    Returns:
        str: The formatted values.
    """
    ...

def otempfile(mode: BinaryModeUpdating) -> IO[bytes]:
    """Opening a temporary file.
    
    Args:
        mode (BinaryModeUpdating): The mode in which the file will be opened.
    
    Returns:
        IO[bytes]: An open file.
    """
    ...

def obytesio(mode: BinaryModeUpdating) -> IO[bytes]:
    """Opening a temporary file.
    
    Args:
        mode (BinaryModeUpdating): The mode in which the file will be opened.
    
    Returns:
        IO[bytes]: An open file.
    """
    ...