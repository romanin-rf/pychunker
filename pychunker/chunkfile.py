import shutil
from pathlib import Path
from tempfile import TemporaryFile
# > Typing
from typing import IO, Union, List, Literal
# > Local Import's
from .chunk import Chunk
from .functions import iocopy, initfp
from .units import DEFAULT_CHUNK_FILE_SIGNATURE

# ! Main Class
class ChunkFile:
    def __ischunkfile(self) -> bool:
        self.__io.seek(0)
        return self.__io.read(len(self.__cfs)) == self.__cfs
    
    def __initchunkfile(self) -> None:
        assert self.__ischunkfile()
        self.__io.seek(len(self.__cfs))
        while len(b_size:=self.__io.read(self.__cls)) != 0:
            size = int.from_bytes(b_size, 'big')
            name = self.__io.read(self.__cns).decode(errors="ignore")
            cio = TemporaryFile("wb+", suffix="chunk")
            iocopy(self.__io, cio, size, buffer_size=self.__bfs)
            self.__chunks.append(
                Chunk(
                    name, cio, self.__mode,
                    chunk_name_size=self.__cns
                )
            )
    
    def __init__(
        self,
        fp: Union[str, Path, IO[bytes]],
        mode: Literal["a", "r", "w"],
        *,
        buffer_size: int=4096,
        chunk_file_signature: bytes=DEFAULT_CHUNK_FILE_SIGNATURE,
        chunk_name_size: int=4,
        chunk_length_size: int=4
    ) -> None:
        """!!! USE THE `ChunkFile.open` METHOD !!!!"""
        self.__name, self.__io = initfp(fp)
        self.__mode = mode
        self.__chunks: List[Chunk] = []
        self.__bfs = buffer_size
        self.__cfs = chunk_file_signature
        self.__cns = chunk_name_size
        self.__cls = chunk_length_size
        
        # ! Initialize Chunk File
        self.__initchunkfile()
    
    @staticmethod
    def create(
        fp: Union[str, Path, IO[bytes]],
        mode: Literal["a", "r", "w"],
        *,
        buffer_size: int=4096,
        chunk_file_signature: bytes=DEFAULT_CHUNK_FILE_SIGNATURE,
        chunk_name_size: int=4,
        chunk_length_size: int=4
    ):
        """!!! USE THE `ChunkFile.open` METHOD !!!!"""
        name, cfio = initfp(fp)
        if not cfio.closed:
            cfio.close()
        cfio = open(name, 'wb+')
        cfio.seek(0)
        cfio.write(chunk_file_signature)
        return ChunkFile(
            cfio, mode,
            buffer_size=buffer_size,
            chunk_file_signature=chunk_file_signature,
            chunk_name_size=chunk_name_size,
            chunk_length_size=chunk_length_size
        )
    
    @staticmethod
    def open( 
        fp: Union[str, Path, IO[bytes]],
        mode: Literal["a", "r", "w"]="r",
        *,
        buffer_size: int=4096,
        chunk_file_signature: bytes=DEFAULT_CHUNK_FILE_SIGNATURE,
        chunk_name_size: int=4,
        chunk_length_size: int=4
    ):
        """
        Opening a chunk file.

        * `mode`: 
        
        \t- `"a"`:  First reads, then opens in read/write mode.
        \t- `"r"`:  Opens in read-only mode.
        \t- `"w"`:  Create a new chunk file, then open in read/write mode.
        """
        if (mode == "r") or (mode == "a"):
            fpopen = ChunkFile
        elif mode == "w":
            fpopen = ChunkFile.create
        else:
            raise ValueError(f"The 'mode' argument cannot be equal: {repr(mode)}")
        return fpopen(
            fp, mode,
            buffer_size=buffer_size,
            chunk_file_signature=chunk_file_signature,
            chunk_name_size=chunk_name_size,
            chunk_length_size=chunk_length_size
        )
    
    # ! Magic Methods
    def __getitem__(self, key: str) -> Chunk:
        for chunk in self.__chunks:
            if key == chunk.name:
                return chunk
        raise KeyError(key)
    
    def __enter__(self): return self
    def __exit__(self, exc_type, exc_value, trace) -> None: self.close()
    
    # ! Vars
    @property
    def chunks(self) -> List[Chunk]: return self.__chunks
    @property
    def mode(self) -> Literal["a", "r", "w"]: return self.__mode
    
    # ! Functions
    def chunk_exists(self, name: str) -> bool:
        for chunk in self.__chunks:
            if chunk.name == name:
                return True
        return False
    
    def create_chunk(self, name: str) -> None:
        assert len(name) <= self.__cns
        assert not self.chunk_exists(name)
        assert self.__mode != "r"
        self.__chunks.append(
            Chunk(
                name.ljust(self.__cns), 
                TemporaryFile("wb+", suffix="chunk"),
                mode=self.__mode,
                chunk_name_size=self.__cns
            )
        )
    
    # ! IO Vars
    @property
    def closed(self) -> bool: return self.__io.closed
    
    # ! IO Functions
    def __ioclear(self) -> None:
        if self.__mode != "r":
            if not self.__io.closed:
                self.__io.close()
            self.__io = open(self.__name, "wb+")
    
    def flush(self) -> None:
        if self.__mode != "r":
            assert not self.__io.closed
            self.__ioclear()
            self.__io.seek(0)
            self.__io.write(self.__cfs)
            for chunk in self.__chunks:
                if not chunk.closed:
                    self.__io.write(chunk.size.to_bytes(self.__cls, 'big'))
                    self.__io.write(chunk.name.encode(errors="ignore"))
                    chunk.seek(0)
                    shutil.copyfileobj(chunk, self.__io)
    
    def close(self) -> None:
        self.flush()
        for chunk in self.__chunks:
            if not chunk.closed:
                chunk.close()
        if not self.__io.closed:
            self.__io.close()
