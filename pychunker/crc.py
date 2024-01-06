import sys
import zlib
from typing import Literal

# ! Main Class
class CRC32:
    """The checksum."""
    def __init__(
        self,
        start_value: int=0,
        byteorder: Literal['little', 'big']=sys.byteorder
    ) -> None:
        """The checksum.
        
        Args:
            start_value (int, optional): The starting value of the checksum. Defaults to 0.
        """
        self.__crc = start_value
        self.__byteorder = byteorder
    
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
        return self.__crc.to_bytes(4, self.__byteorder)
    
    # ! Load Methods
    @staticmethod
    def from_bytes(
        data: bytes,
        byteorder: Literal['little', 'big']=sys.byteorder
    ):
        return CRC32(int.from_bytes(data, byteorder), byteorder)
    
    # ! Main Methods
    def update(self, data: bytes) -> None:
        """Updating the checksum.
        
        Args:
            data (bytes): A byte string for calculating the checksum.
        """
        self.__crc = zlib.crc32(data, self.__crc)
