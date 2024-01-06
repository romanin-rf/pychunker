import os
import sys
from io import DEFAULT_BUFFER_SIZE
from pathlib import Path
# > Local Imports
from .units import CHUNKFILE_MODES
from .crc import CRC32
from .exceptions import IsNotChunkFileModeError

# ! IO Methods
def initfp(fp, mode):
    if isinstance(fp, (str, Path)):
        fp = os.path.abspath(str(fp))
        if mode in ['r', 'r+', '+r']:
            fpmode = 'rb+'
        elif mode in ['w', 'w+', '+w']:
            fpmode = 'wb+'
        else:
            raise IsNotChunkFileModeError(mode)
        return fp, open(fp, fpmode)
    else:
        assert not fp.closed
        assert fp.readable()
        assert fp.seekable()
        assert fp.writable()
        if hasattr(fp, "name"):
            if fp.name is not None:
                return fp.name, fp
        return None, fp

def iocopy(
    from_io,
    to_io,
    size,
    buffer_size=DEFAULT_BUFFER_SIZE,
    byteorder=sys.byteorder
):
    crc = CRC32(byteorder=byteorder)
    while size > 0:
        if size >= buffer_size:
            rsize, size = buffer_size, size - buffer_size
        else:
            rsize, size = size, 0
        d = from_io.read(rsize)
        crc.update(d)
        to_io.write(d)
    return crc

# ! Check Chunkfile Methods
def is_cfmode(value):
    return value in CHUNKFILE_MODES

# ! Check Methods
def hasitem(value, items):
    value = list(value)
    return max([i in value for i in items])

def hasitems(value, items):
    value = list(value)
    return min([i in value for i in items])

# ! Formatting Methods
def formater(**kwargs):
    return ", ".join([f"{key}={repr(value)}" for key, value in kwargs.items()])