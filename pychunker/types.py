from pathlib import Path
from io import BytesIO, BufferedRandom
from typing import (
    TypeVar,
    Generator,
    Union,
    Literal,
    Optional,
    IO,
    Any
)

# ! Type Vars
T = TypeVar('T')
AT = TypeVar('AT')
KT = TypeVar('KT')

# ! Error Types
ErrorTextReturnType = Generator[Optional[str], Any, None]

# ! IO Types
FPType = Union[str, Path, BytesIO, BufferedRandom, IO[bytes]]

# ! Chunk File Modes Types
CFReadMode = Literal['r']
CFWriteMode = Literal['w']
CFReadUpdateMode = Literal['r+', '+r']
CFWriteUpdateMode = Literal['w+', '+w']
CFMode = Union[CFReadMode, CFReadUpdateMode, CFWriteMode, CFWriteUpdateMode]