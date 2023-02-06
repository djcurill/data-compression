from typing import List, Union
from src.lossless.decoders.base_decoder import Decoder
from bitarray import bitarray

Data = Union[str, int, float]
Bits = bitarray


def decompress_array(data: List[Bits], decoder: Decoder) -> List[Data]:
    return [decoder(bit) for bit in data]


def decompress(bits: Bits, decoder: Decoder) -> List[Data]:
    pos = 0
    res = []
    while pos < len(bits):
        symbol, pos = decoder(bits, start=pos)
        res.append(symbol)
    return res
