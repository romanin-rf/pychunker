from .crc import CRC32
from .chunkfile import ChunkFile
from .exceptions import (
    IOReadOnlyError,
    ChunkIsDamagedError,
    IsNotChunkFile
)

open = ChunkFile.open