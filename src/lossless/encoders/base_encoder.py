from typing import Union
from abc import ABC, abstractmethod
from bitarray import bitarray

Symbol = Union[str, int]


class Encoder(ABC):
    @abstractmethod
    def __call__(self, symbol: Symbol) -> bitarray:
        pass
