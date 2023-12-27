import zlib

# ! Main Class
class CRC32:
    def __init__(self, start_value: int=0) -> None:
        self.__crc = start_value
    
    # ! Magic Methods
    def __str__(self) -> str:
        return str(self.__crc)
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.__str__()})"
    
    def __int__(self) -> int:
        return self.__crc
    
    def __hex__(self) -> str:
        return hex(self.__crc)
    
    def __bytes__(self) -> bytes:
        return self.__crc.to_bytes(4, "big")
    
    # ! Main Methods
    def update(self, data: bytes) -> None:
        self.__crc = zlib.crc32(data, self.__crc)
