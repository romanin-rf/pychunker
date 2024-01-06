import io
import sys
from typing import Callable, IO, Literal
from .chunkfile import ChunkFile, otempfile
from .types import FPType, CFMode
from .units import DEFAULT_CHUNK_FILE_SIGNATURE

# ! Main Open Method
def open(
    fp: FPType,
    mode: CFMode='r',
    *,
    buffer_size: int=io.DEFAULT_BUFFER_SIZE,
    chunk_file_signature: bytes=DEFAULT_CHUNK_FILE_SIGNATURE,
    chunk_name_size: int=4,
    chunk_length_size: int=4,
    openio: Callable[[], IO[bytes]]=otempfile,
    encoding: str='utf-8',
    errors: str='strict',
    byteorder: Literal['little', 'big']=sys.byteorder,
    ignore_crc: bool=False
) -> ChunkFile:
    """Opening a chunkfile.
    
    Args:
        fp (FPType): The path or an already open IO.
        mode (CFMode, optional): The mode in which the file will be opened. Defaults to 'r'.
        buffer_size (int, optional): The size of the buffer. Defaults to io.DEFAULT_BUFFER_SIZE.
        chunk_file_signature (bytes, optional): The signature of the chunk file. Defaults to DEFAULT_CHUNK_FILE_SIGNATURE.
        chunk_name_size (int, optional): The length of the chunk name. Defaults to 4.
        chunk_length_size (int, optional): The number of bytes with the specified chunk size. Defaults to 4.
        openio (Callable[[], IO[bytes]], optional): The function of opening a temporary file. Defaults to otempfile.
        encoding (str, optional): The name of the encoding used to decode the stream bytes into strings, and to encode strings into bytes. Defaults to 'utf-8'.
        errors (str, optional): The error setting of the decoder or encoder. Defaults to 'strict'.
        byteorder (Literal['little', 'big'], optional): An indicator of the native byte order. Defaults to sys.byteorder.
        ignore_crc (bool, optional): If True, then checksum verification does not occur. Defaults to False.
    
    Returns:
        ChunkFile: A chunkfile.
    """
    ...
