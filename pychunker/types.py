from typing import Literal, Union

# ! IO Modes
TextModeUpdating = Literal["r+", "+r", "rt+", "r+t", "+rt", "tr+", "t+r", "+tr", "w+", "+w", "wt+", "w+t", "+wt", "tw+", "t+w", "+tw", "a+", "+a", "at+", "a+t", "+at", "ta+", "t+a", "+ta", "x+", "+x", "xt+", "x+t", "+xt", "tx+", "t+x", "+tx"]
TextModeWriting = Literal["w", "wt", "tw", "a", "at", "ta", "x", "xt", "tx"]
TextModeReading = Literal["r", "rt", "tr", "U", "rU", "Ur", "rtU", "rUt", "Urt", "trU", "tUr", "Utr"]
BinaryModeUpdating = Literal["rb+", "r+b", "+rb", "br+", "b+r", "+br", "wb+", "w+b", "+wb", "bw+", "b+w", "+bw", "ab+", "a+b", "+ab", "ba+", "b+a", "+ba", "xb+", "x+b", "+xb", "bx+", "b+x", "+bx"]
BinaryModeWriting = Literal["wb", "bw", "ab", "ba", "xb", "bx"]
BinaryModeReading = Literal["rb", "br", "rbU", "rUb", "Urb", "brU", "bUr", "Ubr"]
TextMode = Union[TextModeUpdating, TextModeWriting, TextModeReading]
BinaryMode = Union[BinaryModeUpdating, BinaryModeWriting, BinaryModeReading]
CFReadMode = Literal['r']
CFWriteMode = Literal['w']
CFUpdateMode = Literal['a']
CFMode = Union[CFReadMode, CFWriteMode, CFUpdateMode]