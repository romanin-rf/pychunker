from typing import Generator, Any, Optional, Tuple

# ! Base Class
class ErrorBase(Exception):
    """ """
    def __init__(self, *args, **kwargs) -> None:
        """ """
        self.__init__()
        self.args: Tuple[str, ...] = tuple([arg for arg in self.exception(*args, **kwargs) if arg is not None])
    
    def exception(self, *args, **kwargs) -> Generator[Optional[str], Any, None]:
        yield None

# ! ChunkFile Errors
class ChunkIsDamagedError(ErrorBase):
    def exception(self, file_crc: int, chunk_crc: int, *args, **kwargs):
        yield f"The checksum of the read chunk does not match the checksum of the one written in the chunk file ({repr(file_crc)} != {repr(chunk_crc)})."

class IsNotChunkFile(ErrorBase):
    def exception(self, *args, **kwargs):
        yield "The signature of the file is not equal to the signature of the specified chunk file."

# ! IO Errors
class IOReadOnlyError(ErrorBase):
    def exception(self, *args, **kwargs):
        yield "This IO is open in read-only mode."