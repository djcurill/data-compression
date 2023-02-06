from src.core.dist import Dist
from typing import List
import random
from bitarray import bitarray

POPULATION = bytearray(list(range(0,128)))

def to_binary(n:int) -> bitarray:
    if n <= 1:
        return bitarray(str(n))
    return to_binary(n // 2) + bitarray(str(n % 2))

def generate_random_data(n:int, p:float=0.5) -> List[bytes]:
    res = []
    byte = random.choice(POPULATION)
    for i in range(n):
        if random.uniform(0,1) > p:
            # select a new byte
            byte = random.choice(POPULATION)
        res.append(byte)
    return res

def number_of_bits(data:bytes) -> int:
    """Return number of bits to represent data"""
    bits = bitarray(endian="little")
    bits.frombytes(data)
    return len(bits)



