# Chunker
## Description
Module for reading/writing chunk files.

## Installation
```
pip install pychunker
```

## Using
- `example.py`:
```python
import pychunker

with pychunker.opencf("chunkfile.bin", "w") as cf:
    with cf.create_chunk("DDAT") as ddat:
        ddat.write(b'1234567890')
    
    with cf.create_chunk("SDAT") as sdat:
        sdat.write(b'Hello World!')

with pychunker.opencf("chunkfile.bin") as cf:
    print(cf.chunks)
```

- `output`:
```python
>>> [Chunk(name='DDAT', mode='a', size=10), Chunk(name='SDAT', mode='a', size=12)]
```