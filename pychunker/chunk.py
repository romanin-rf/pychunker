# > Typing
from typing import IO, List, Iterable, Optional, Literal

# ! Main Class
class Chunk:
    def __init__(
        self,
        name: str,
        io: IO[bytes],
        mode: Literal["a", "r", "w"],
        *,
        chunk_name_size: int=4
    ) -> None:
        self.__name: str = name
        self.__mode: Literal["a", "r", "w"] = mode
        self.__io: IO[bytes] = io
        self.__cns: int = chunk_name_size
    
    # ! Magic Methods
    def __str__(self) -> str: return f"{self.__class__.__name__}(name={repr(self.__name)}, mode={repr(self.__mode)}, size={repr(self.size)})"
    def __repr__(self) -> str: return self.__str__()
    def __enter__(self): return self
    def __exit__(self, exc_type, exc_value, trace) -> None:
        if not self.closed:
            self.close()
    
    # ! Property
    @property
    def name(self) -> str: return self.__name
    
    @property
    def mode(self) -> Literal["a", "r", "w"]: return self.__mode
    
    @property
    def size(self) -> int:
        cp = self.__io.tell()
        self.__io.seek(0, 2)
        s = self.__io.tell()
        self.__io.seek(cp)
        return s
    
    # ! Chunk Functions
    def rename(self, name: str) -> None:
        assert len(name) <= self.__cns
        self.__name = name.ljust(self.__cns)
    
    # ! IO Vars
    @property
    def closed(self) -> bool: return self.__io.closed
    
    # ! IO Functions
    def readable(self) -> bool: return True and (not self.__io.closed)
    def seekable(self) -> bool: return True and (not self.__io.closed)
    def writable(self) -> bool: return True and (not self.__io.closed) and (self.__mode != "r")
    
    def read(self, __n: int=-1) -> bytes: return self.__io.read(__n)
    def readline(self, __limit: int=-1) -> bytes: return self.__io.readline(__limit)
    def readlines(self, __hint: int=-1) -> List[bytes]: return self.__io.readlines(__hint)
    
    def tell(self) -> int: return self.__io.tell()
    def seek(self, __offset: int, __whence: int=0) -> int: return self.__io.seek(__offset, __whence)
    
    def write(self, __s: bytes) -> int:
        assert self.__mode != "r"
        return self.__io.write(__s)
    def writelines(self, __lines: Iterable[bytes]) -> None:
        assert self.__mode != "r"
        return self.__io.writelines(__lines)
    def flush(self) -> None:
        assert self.__mode != "r"
        return self.__io.flush()
    def truncate(self, __size: Optional[int]=None) -> int:
        assert self.__mode != "r"
        return self.__io.truncate(__size)
    
    def close(self) -> None: return self.__io.close()
