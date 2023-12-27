import os
from pathlib import Path
from tempfile import TemporaryFile
from io import BytesIO, DEFAULT_BUFFER_SIZE
from .crc import CRC32

# ! IO Methods
def initfp(fp, needed_mode='a'):
    assert needed_mode in ('r', 'w', 'a')
    if isinstance(fp, (str, Path)):
        path = os.path.abspath(str(Path(fp)))
        if os.path.exists(path):
            assert os.path.isfile(path)
            if needed_mode == 'r':
                return path, open(path, 'rb')
            return path, open(path, 'rb+')
        return path, open(path, 'wb+')
    else:
        assert not fp.closed
        if needed_mode == "r" or needed_mode == "a":
            assert fp.readable()
            assert fp.seekable()
        if needed_mode == "w" or needed_mode == "a":
            assert fp.writable()
        if hasattr(fp, "name"):
            if isinstance(fp.name, str):
                return fp.name, fp
        return None, fp

def iocopy(from_io, to_io, size, buffer_size=DEFAULT_BUFFER_SIZE):
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

def otempfile(mode):
    return TemporaryFile(mode, suffix="chunk")

def obytesio(mode):
    return BytesIO()

# ! Formattins Methods
def formater(**kwargs: object) -> str:
    return ", ".join([f"{key}={repr(value)}" for key, value in kwargs.items()])