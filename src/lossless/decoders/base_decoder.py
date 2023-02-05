from typing import Union, Tuple
from abc import ABC, abstractmethod
from bitarray import bitarray

Symbol = Union[str, int]

class Decoder(ABC):

    @abstractmethod
    def __call__(self, bits:bitarray, **kwargs) -> Tuple[Symbol, int]:
        pass