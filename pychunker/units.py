from typing import List, Literal

DEFAULT_CHUNK_FILE_SIGNATURE: bytes = b"\x89CHKFL\r\n"
"""The default signature of the chunkfile."""
CHUNKFILE_MODES = ['r', 'r+', '+r', 'w', 'w+', '+w']
"""Modes for opening a chunkfile."""