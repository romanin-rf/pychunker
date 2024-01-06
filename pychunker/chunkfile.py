import sys
from tempfile import TemporaryFile
from io import BytesIO, DEFAULT_BUFFER_SIZE
# > Typing
from types import TracebackType
from typing import Optional, IO, Callable, Literal, List
# > Local Imports
from .crc import CRC32
from .chunk import Chunk
from .types import CFMode, FPType
from .units import DEFAULT_CHUNK_FILE_SIGNATURE
from .functional import initfp, is_cfmode, iocopy, hasitem, formater
from .exceptions import IsNotChunkFileError, IONotWritableError, ChunkIsDamagedError

# ! Main Class Functions
def otempfile():
    return TemporaryFile("wb+", suffix="chunk")

def obytesio():
    return BytesIO()

# ! Main Class
class ChunkFile:
    # ! Private Initialization Methods
    def __ischunkfile(self) -> bool:
        self.__io.seek(0)
        return self.__io.read(len(self.__cfs)) == self.__cfs
    
    def __initchunkfile(self) -> None:
        if not self.__ischunkfile():
            return IsNotChunkFileError()
        self.__io.seek(len(self.__cfs))
        size_data = self.__io.read(self.__cls)
        while len(size_data) > 0:
            size = int.from_bytes(size_data, self.__bord)
            name = self.__io.read(self.__cns).decode(self.__encoding, self.__errors)
            cio = self.__openio()
            currect_crc = iocopy(self.__io, cio, size, self.__bfs, self.__bord)
            file_crc = CRC32.from_bytes(self.__io.read(4), self.__bord)
            if (int(file_crc) != int(currect_crc)) and (not self.__icrc):
                raise ChunkIsDamagedError()
            self.__chunks.append(Chunk(name, cio, self.__mode, chunk_name_size=self.__cns))
            size_data = self.__io.read(self.__cls)
    
    # ! Initialization
    def __init__(
        self,
        fp: FPType,
        mode: CFMode='r',
        *,
        buffer_size: int=DEFAULT_BUFFER_SIZE,
        chunk_file_signature: bytes=DEFAULT_CHUNK_FILE_SIGNATURE,
        chunk_name_size: int=4,
        chunk_length_size: int=4,
        openio: Callable[[], IO[bytes]]=otempfile,
        encoding: str='utf-8',
        errors: str='strict',
        byteorder: Literal['little', 'big']=sys.byteorder,
        ignore_crc: bool=False
    ) -> None:
        assert is_cfmode(mode)
        self.__name, self.__io = initfp(fp, mode)
        self.__mode = mode
        self.__chunks: List[Chunk] = []
        self.__bfs: int = buffer_size
        self.__cfs: bytes = chunk_file_signature
        self.__cns: int = chunk_name_size
        self.__cls: int = chunk_length_size
        self.__openio = openio
        self.__encoding = encoding
        self.__errors = errors
        self.__bord = byteorder
        self.__icrc: bool = ignore_crc
        self.__initchunkfile()
    
    # ! ChunkFile Private Methods
    def __GetChunk(self, name: str) -> Optional[Chunk]:
        for chunk in self.__chunks:
            if chunk.name == name:
                return chunk
    
    # ! Magic Methods
    def __str__(self) -> str:
        return formater(name=self.__name, mode=self.__mode)
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.__str__()})"
    
    def __getitem__(self, key: str):
        chunk = self.__GetChunk(key)
        if chunk is None:
            if not self.writable():
                raise IONotWritableError()
            chunk = Chunk(key, self.__openio(), self.__mode)
            self.__chunks.append(chunk)
        return chunk
    
    def __enter__(self):
        return self
    
    def __exit__(
        self,
        exc_type: Optional[type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType]
    ) -> None:
        self.close()
    
    # ! Private IO Methods
    def __ioflush(self) -> None:
        self.__ioclear()
        self.__io.seek(0)
        self.__io.write(self.__cfs)
        for chunk in self.__chunks:
            if not chunk.closed:
                self.__io.write(chunk.size.to_bytes(self.__cls, self.__bord))
                self.__io.write(chunk.name.encode(self.__encoding, self.__errors))
                chunk.seek(0)
                crc = iocopy(chunk._io, self.__io, chunk.size, self.__bfs, self.__bord)
                self.__io.write(bytes(crc))
    
    def __ioclear(self) -> None:
        self.__io.seek(0)
        self.__io.truncate(0)
    
    # ! Propertyes
    @property
    def name(self) -> Optional[str]:
        return self.__name
    
    @property
    def mode(self) -> CFMode:
        return self.__mode
    
    @property
    def chunks(self) -> List[Chunk]:
        return self.__chunks
    
    # ! ChunkFile Methods
    def chunk(self, name: str) -> Chunk:
        return self.__getitem__(name)
    
    # ! IO Methods
    def readable(self) -> bool:
        return hasitem(self.__mode, 'r+')
    
    def seekable(self) -> bool:
        return self.__io.seekable()
    
    def writable(self) -> bool:
        return hasitem(self.__mode, 'w+')
    
    def flush(self) -> None:
        assert not self.__io.closed
        if not self.writable():
            raise IONotWritableError()
        self.__ioflush()
    
    def close(self) -> None:
        if self.writable():
            self.flush()
        for chunk in self.__chunks:
            if not chunk.closed:
                chunk.close()
        if not self.__io.closed:
            self.__io.close()