from typing import Generic
from .types import AT, KT, ErrorTextReturnType
from .units import CHUNKFILE_MODES

# ! Base Error Class
class Error(Exception, Generic[AT, KT]):
    """The base class of the error."""
    def __init__(self, *args: AT, **kwargs: KT) -> None:
        """The base class of the error."""
        super().__init__()
        self.args = tuple(" ".join([arg for arg in self.__text__(*args, **kwargs) if arg is not None]))
    
    def __text__(self, *args: AT, **kwargs: KT) -> ErrorTextReturnType:
        """Error text generator.
        
        Returns:
            ErrorTextReturnType: A generator with strings.
        """
        yield

# ! Chunkfile Errors
class IsNotChunkFileError(Error):
    def __text__(self, *args, **kwargs):
        yield "The IO you have opened is not a chunkfile."

class IsNotChunkFileModeError(Error[str, str]):
    def __text__(self, mode: str, *args, **kwargs):
        yield f"This mode value is not supported by the chunkfile: {repr(mode)}."
        yield f"Use anyone from this list: {', '.join([repr(cfmode) for cfmode in CHUNKFILE_MODES])}."

class ChunkIsDamagedError(Error):
    def __text__(self, *args, **kwargs):
        yield "The chunk is damaged."

# ! IO Errors
class IONotWritableError(Error):
    def __text__(self, *args, **kwargs):
        yield "This IO is open in a mode that does not provide for writing."