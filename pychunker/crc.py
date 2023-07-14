import zlib

# ! Main Class
class CRC32:
    def __init__(self, start_value: int=0) -> None:
        self.__crc = start_value
    
    # ! Property
    @property
    def crc(self) -> int: return self.__crc
    @property
    def crc_hex(self) -> int: return hex(self.__crc)
    @property
    def crc_bytes(self) -> bytes: return self.__crc.to_bytes(4, "big")
    
    # ! Magic Methods
    def __str__(self) -> str: return f"{self.__class__.__name__}(crc={repr(self.crc)}, crc_hex={repr(self.crc_hex)}, crc_bytes={repr(self.crc_bytes)})"
    def __repr__(self) -> str: return self.__str__()
    
    # ! CRC32 Methods
    def update(self, data: bytes) -> None:
        self.__crc = zlib.crc32(data, self.__crc)
