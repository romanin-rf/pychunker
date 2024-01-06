import sys
from io import DEFAULT_BUFFER_SIZE
from typing import Callable, IO, Literal
from .chunkfile import ChunkFile, otempfile
from .types import FPType, CFMode
from .units import DEFAULT_CHUNK_FILE_SIGNATURE

# ! Main Open Method
def open(*args, **kwargs):
    return ChunkFile(*args, **kwargs)

"""Opening a chunkfile.
    
    Args:
        fp (FPType): The path or an already open IO.
        mode (CFMode, optional): The mode in which the file will be opened. Defaults to 'r'.
        buffer_size (int, optional): The size of the buffer. Defaults to DEFAULT_BUFFER_SIZE.
        chunk_file_signature (bytes, optional): The signature of the chunk file. Defaults to DEFAULT_CHUNK_FILE_SIGNATURE.
        chunk_name_size (int, optional): The length of the chunk name. Defaults to 4.
        chunk_length_size (int, optional): The number of bytes with the specified chunk size. Defaults to 4.
        ignore_crc (bool, optional): If True, then checksum verification does not occur. Defaults to False.
        openio (Callable[[], IO[bytes]], optional): The function of opening a temporary file. Defaults to otempfile.
    
    Returns:
        ChunkFile: A chunkfile.
    """