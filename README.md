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

with pychunker.open("chunkfile.bin", "w") as cf:
    # The chunk can be used via `with'.
    with cf.chunk("DDAT") as ddat:
        ddat.write(b'1234567890')
    
    # Or by contacting the key (name of the chunk).
    cf["SDAT"].write(b'Hello World!')

# !!! Attention !!!
# Both types of treatment use the same methods,
# namely that if you open a chunk file in read-only mode,
# and if the chunk is not in the chunk file,
# he will try to create a chunk,
# but he will not be able to do this and will give a `IONotWritableError`.

with pychunker.open("chunkfile.bin") as cf:
    print(cf.chunks)
```

- `Output`:
```python
[Chunk(name='DDAT', mode='r', size=10), Chunk(name='SDAT', mode='r', size=12)]
```