# Chunker
## Description
Module for reading/writing chunk files.

## Using
- `example.py`:
```python
import pychunker

with pychunker.open("chunkfile.bin", "w") as cf:
    with cf.create_chunk("DDAT") as ddat:
        ddat.write(b'1234567890')
    
    with cf.create_chunk("SDAT") as sdat:
        sdat.write(b'Hello World!')

with pychunker.open("chunkfile.bin") as cf:
    print(cf.chunks)
```

- `output`:
```python
>>> [Chunk(name='DDAT', mode='r', size=10), Chunk(name='SDAT', mode='r', size=12)]
```