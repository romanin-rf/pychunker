import os
from pathlib import Path
from .crc import CRC32

# ! Functions
def initfp(fp):
    if isinstance(fp, str) or isinstance(fp, Path):
        path = str(Path(fp))
        if os.path.exists(path):
            assert os.path.isfile(path)
            return str(path), open(path, 'rb+')
        else:
            return str(path), open(path, 'wb+')
    else:
        assert not fp.closed
        assert fp.readable()
        assert fp.seekable()
        assert fp.writable()
        assert hasattr(fp, "name")
        assert isinstance(fp.name, str)
        return fp.name, fp

def iocopy(from_io, to_io, size, buffer_size=8192):
    crc = CRC32()
    while size > 0:
        if size >= buffer_size:
            rsize, size = buffer_size, size - buffer_size
        else:
            rsize, size = size, 0
        d: bytes = from_io.read(rsize)
        crc.update(d)
        to_io.write(d)
    return crc