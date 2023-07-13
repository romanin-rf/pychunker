# Chunker
## Description
Module for reading/writing chunk files.

## Using
- `exmaple.py`:
```python
import pychunker

with pychunker.open("chunkfile.bin", "w") as cf:
    cf.create_chunk("ADAT")
    cf.create_chunk("STR_")
    
    cf["ADAT"].write(b'1234567890')
    cf["STR_"].write(b'STRING')

with pychunker.open("chunkfile.bin") as cf:
    print(cf.chunks)
```

- `output`:
```python
>>> [Chunk(name='ADAT', mode='r', size=10), Chunk(name='STR_', mode='r', size=6)]
```