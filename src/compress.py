from typing import List, Union
from src.lossless.encoders.base_encoder import Encoder
from bitarray import bitarray

Data = Union[str, int, float]
Bits = bitarray
Bytes = bytes


def compress_to_array(data: List[Data], encoder: Encoder) -> List[Bits]:
    return [encoder(symbol) for symbol in data]


def compress_bytes(data: List[Data], encoder: Encoder) -> Bytes:
    bits = bitarray()
    for symbol in data:
        bits += encoder(symbol)
    return bits
