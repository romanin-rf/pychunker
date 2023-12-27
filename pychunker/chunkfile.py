from pathlib import Path
from io import BytesIO, DEFAULT_BUFFER_SIZE
# > Typing
from typing import IO, Union, List, Literal, Callable, final
# > Local Import's
from .types import CFMode, BinaryModeUpdating
from .chunk import Chunk
from .units import DEFAULT_CHUNK_FILE_SIGNATURE
from .functions import (
    iocopy, initfp, otempfile, formater
)
from .exceptions import (
    ChunkIsDamagedError,
    IsNotChunkFile,
    IOReadOnlyError
)

# ! Main Class
@final
class ChunkFile:
    """The class of the chunk file."""
    def __ischunkfile(self) -> bool:
        self.__io.seek(0)
        return self.__io.read(len(self.__cfs)) == self.__cfs
    
    def __initchunkfile(self) -> None:
        if not self.__ischunkfile():
            raise IsNotChunkFile()
        
        self.__io.seek(len(self.__cfs))
        
        while len(b_size:=self.__io.read(self.__cls)) != 0:
            cio = self.__coiom("w+b")
            size = int.from_bytes(b_size, 'big')
            name = self.__io.read(self.__cns).decode(errors="ignore")
            
            ccrc = iocopy(self.__io, cio, size, self.__bfs)
            fcrc = int.from_bytes(self.__io.read(4), 'big')
            
            if fcrc == int(ccrc):
                self.__chunks.append(
                    Chunk(
                        name, cio, self.__mode,
                        chunk_name_size=self.__cns
                    )
                )
            else:
                if not self.__icrc:
                    raise ChunkIsDamagedError(fcrc, ccrc)
    
    def __init__(
        self,
        fp: Union[str, Path, IO[bytes]],
        mode: CFMode,
        *,
        buffer_size: int=DEFAULT_BUFFER_SIZE,
        chunk_file_signature: bytes=DEFAULT_CHUNK_FILE_SIGNATURE,
        chunk_name_size: int=4,
        chunk_length_size: int=4,
        ignore_crc: bool=False,
        openio: Callable[[BinaryModeUpdating], IO[bytes]]=otempfile,
    ) -> None:
        """The class of the chunk file (`!!! USE THE 'open' METHOD !!!`).
        
        Args:
            fp (Union[str, Path, IO[bytes]]): The path or the open file.
            mode (CFMode, optional): The access mode of opening the file. Defaults to "r".
            buffer_size (int, optional): The size of the temporary buffer. Defaults to 8192.
            chunk_file_signature (bytes, optional): The signature of the chunk file. Defaults to DEFAULT_CHUNK_FILE_SIGNATURE.
            chunk_name_size (int, optional): The length of the chunk name. Defaults to 4.
            chunk_length_size (int, optional): The length of the byte string indicating the size of the data in the chunk. Defaults to 4.
            ignore_crc (bool, optional): Ignore the checksum (CRC32). Defaults to False.
            openio (Callable[[BinaryModeUpdating], IO[bytes]], optional): A function that opens a temporary IO for a chunk. Defaults to otempfile.
        
        Raises:
            IsNotChunkFile: Called if the file is not a chunk file.
            ChunkIsDamagedError: Called if the checksum does not match when reading chunks.
        """
        self.__name, self.__io = initfp(fp, mode)
        self.__mode: Literal["a", "r", "w"] = mode
        self.__chunks: List[Chunk] = []
        self.__bfs: int = buffer_size
        self.__cfs: bytes = chunk_file_signature
        self.__cns: int = chunk_name_size
        self.__cls: int = chunk_length_size
        self.__coiom = openio
        self.__icrc = ignore_crc
        
        # ! Initialize Chunk File
        self.__initchunkfile()
    
    @staticmethod
    def create(
        fp: Union[str, Path, IO[bytes]],
        mode: CFMode,
        *,
        buffer_size: int=DEFAULT_BUFFER_SIZE,
        chunk_file_signature: bytes=DEFAULT_CHUNK_FILE_SIGNATURE,
        chunk_name_size: int=4,
        chunk_length_size: int=4,
        ignore_crc: bool=False,
        openio: Callable[[BinaryModeUpdating], IO[bytes]]=otempfile
    ):
        """The class of the chunk file (`!!! USE THE 'open' METHOD !!!`).
        
        Args:
            fp (Union[str, Path, IO[bytes]]): The path or the open file.
            mode (CFMode, optional): The access mode of opening the file. Defaults to "r".
            buffer_size (int, optional): The size of the temporary buffer. Defaults to 8192.
            chunk_file_signature (bytes, optional): The signature of the chunk file. Defaults to DEFAULT_CHUNK_FILE_SIGNATURE.
            chunk_name_size (int, optional): The length of the chunk name. Defaults to 4.
            chunk_length_size (int, optional): The length of the byte string indicating the size of the data in the chunk. Defaults to 4.
            ignore_crc (bool, optional): Ignore the checksum (CRC32). Defaults to False.
            openio (Callable[[BinaryModeUpdating], IO[bytes]], optional): A function that opens a temporary IO for a chunk. Defaults to otempfile.
        
        Raises:
            IsNotChunkFile: Called if the file is not a chunk file.
            ChunkIsDamagedError: Called if the checksum does not match when reading chunks.
        
        Returns:
            ChunkFile: The class of the chunk file.
        """
        name, cfio = initfp(fp, mode)
        
        cfio.seek(0)
        cfio.write(chunk_file_signature)
        
        return ChunkFile(
            cfio, mode,
            buffer_size=buffer_size,
            chunk_file_signature=chunk_file_signature,
            chunk_name_size=chunk_name_size,
            chunk_length_size=chunk_length_size,
            ignore_crc=ignore_crc,
            openio=openio
        )
    
    # ! Magic Methods
    def __str__(self) -> str:
        return f"{self.__class__.__name__}({formater(name=self.__name, mode=self.__mode)})"
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __getitem__(self, key: str) -> Chunk:
        for chunk in self.__chunks:
            if key == chunk.name:
                return chunk
        raise KeyError(key)
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, trace) -> None:
        self.close()
    
    # ! Vars
    @property
    def name(self) -> str:
        """The path to the file.
        
        Returns:
            str: This filepath.
        """
        return self.__name
    
    @property
    def chunks(self) -> List[Chunk]:
        """A list of chunks.
        
        Returns:
            List[Chunk]: A list of chunks.
        """
        return self.__chunks
    
    @property
    def mode(self) -> CFMode:
        return self.__mode
    
    # ! Functions
    def exists_chunk(self, name: str) -> bool:
        for chunk in self.__chunks:
            if chunk.name == name:
                return True
        return False
    
    def get_chunk(self, name: str) -> Chunk:
        return self.__getitem__(name)
    
    def create_chunk(self, name: str) -> Chunk:
        assert len(name) <= self.__cns
        assert not self.exists_chunk(name)
        if self.mode == "r":
            raise IOReadOnlyError()
        chunk = Chunk(
            name.ljust(self.__cns), 
            self.__coiom("wb+"),
            mode=self.__mode,
            chunk_name_size=self.__cns
        )
        self.__chunks.append(chunk)
        return chunk
    
    # ! IO Vars
    @property
    def closed(self) -> bool:
        return self.__io.closed
    
    # ! IO Functions
    def __ioclear(self) -> None:
        if self.__mode != "r":
            if not self.__io.closed:
                self.__io.close()
            if self.__name is not None:
                self.__io = open(self.__name, "wb+")
            else:
                self.__io = BytesIO()
        else:
            raise IOReadOnlyError()
    
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
                    crc = iocopy(chunk, self.__io, chunk.size)
                    self.__io.write(bytes(crc))
        else:
            raise IOReadOnlyError()
    
    def close(self) -> None:
        if self.__mode != "r":
            self.flush()
        for chunk in self.__chunks:
            if not chunk.closed:
                chunk.close()
        if not self.__io.closed:
            self.__io.close()

# ! Main Open Method
def opencf(
    fp: Union[str, Path, IO[bytes]],
    mode: CFMode="a",
    *,
    buffer_size: int=DEFAULT_BUFFER_SIZE,
    chunk_file_signature: bytes=DEFAULT_CHUNK_FILE_SIGNATURE,
    chunk_name_size: int=4,
    chunk_length_size: int=4,
    ignore_crc: bool=False,
    openio: Callable[[BinaryModeUpdating], IO[bytes]]=otempfile
) -> ChunkFile:
    """Opening a chuck file.
    
    Args:
        fp (Union[str, Path, IO[bytes]]): The path or the open file.
        mode (CFMode, optional): The access mode of opening the file. Defaults to "r".
        buffer_size (int, optional): The size of the temporary buffer. Defaults to 8192.
        chunk_file_signature (bytes, optional): The signature of the chunk file. Defaults to DEFAULT_CHUNK_FILE_SIGNATURE.
        chunk_name_size (int, optional): The length of the chunk name. Defaults to 4.
        chunk_length_size (int, optional): The length of the byte string indicating the size of the data in the chunk. Defaults to 4.
        ignore_crc (bool, optional): Ignore the checksum (CRC32). Defaults to False.
        openio (Callable[[BinaryModeUpdating], IO[bytes]], optional): A function that opens a temporary IO for a chunk. Defaults to otempfile.
    
    Raises:
        IsNotChunkFile: Called if the file is not a chunk file.
        ChunkIsDamagedError: Called if the checksum does not match when reading chunks.
        ValueError: Called if 'mode' was specified incorrectly.
    
    Returns:
        ChuckFile: The class of the chunk file.
    """
    if (mode == "r") or (mode == "a"):
        fpopen = ChunkFile
    elif mode == "w":
        fpopen = ChunkFile.create
    else:
        raise ValueError(f"The 'mode' argument cannot be equal: {repr(mode)}.")
    return fpopen(
        fp, mode,
        buffer_size=buffer_size,
        chunk_file_signature=chunk_file_signature,
        chunk_name_size=chunk_name_size,
        chunk_length_size=chunk_length_size,
        ignore_crc=ignore_crc,
        openio=openio
    )