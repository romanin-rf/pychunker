from types import TracebackType
from typing import IO, List, Iterable, Optional
# > Local Imports
from .types import CFMode
from .functional import is_cfmode, hasitem, formater

# ! Main Class
class Chunk:
    """The chunk."""
    def __init__(
        self,
        name: str,
        io: IO[bytes],
        mode: CFMode,
        *,
        chunk_name_size: int=4
    ) -> None:
        """Opening a chunk.
        
        Args:
            name (str): The name of the chunk.
            io (IO[bytes]): IO with chunk data.
            mode (CFMode): The mode of opening the chunk.
            chunk_name_size (int, optional): The length of the chunk name. Defaults to 4.
        """
        assert is_cfmode(mode)
        self.__io = io
        self.__mode = mode
        self.__name = name
        self.__cns = chunk_name_size
    
    # ! Propertyes
    @property
    def name(self) -> str:
        """The name of the chunk.
        
        Returns:
            str: The name of the chunk.
        """
        return self.__name
    
    @property
    def mode(self) -> CFMode:
        """The mode in which the chunk is open.
        
        Returns:
            CFMode: The mode in which the chunk is open.
        """
        return self.__mode
    
    @property
    def size(self) -> int:
        """The current size of the chunk data in bytes.
        
        Returns:
            int: The current size of the chunk data in bytes.
        """
        cp = self.__io.tell()
        self.__io.seek(0, 2)
        s = self.__io.tell()
        self.__io.seek(cp)
        return s
    
    @property
    def closed(self) -> bool:
        return self.__io.closed
    
    @property
    def _io(self) -> IO[bytes]:
        return self.__io
    
    # ! Magic Methods
    def __str__(self) -> str:
        return formater(name=self.__name, mode=self.__mode)
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.__str__()})"
    
    def __enter__(self):
        return self
    
    def __exit__(
        self,
        exc_type: Optional[type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType]
    ) -> None:
        pass
    
    # ! Chunk Methods
    def rename(self, name: str) -> None:
        assert len(name) <= self.__cns
        self.__name = name.ljust(self.__cns)
    
    # ! Main IO Methods
    def readable(self) -> bool:
        return hasitem(self.__mode, ['r', '+'])
    
    def seekable(self) -> bool:
        return self.__io.seekable()
    
    def writable(self) -> bool:
        return hasitem(self.__mode, ['w', '+'])
    
    def read(self, __n: int=-1) -> bytes:
        assert self.readable()
        return self.__io.read(__n)
    
    def readline(self, __limit: int=-1) -> bytes:
        assert self.readable()
        return self.__io.readline(__limit)
    
    def readlines(self, __hint: int=-1) -> List[bytes]:
        assert self.readable()
        return self.__io.readlines(__hint)
    
    def tell(self) -> int:
        return self.__io.tell()
    
    def seek(self, __offset: int, __whence: int=0) -> int:
        assert self.seekable()
        return self.__io.seek(__offset, __whence)
    
    def write(self, __s: bytes) -> int:
        assert self.writable()
        return self.__io.write(__s)
    
    def writelines(self, __lines: Iterable[bytes]) -> None:
        assert self.writable()
        return self.__io.writelines(__lines)
    
    def flush(self) -> None:
        assert self.writable()
        return self.__io.flush()
    
    def truncate(self, __size: Optional[int]=None) -> int:
        assert self.seekable()
        assert self.writable()
        return self.__io.truncate(__size)
    
    def close(self) -> None:
        return self.__io.close()
