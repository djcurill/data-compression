from bitarray import bitarray
from src.core.tree import HuffmanTree
from src.lossless.decoders.base_decoder import Decoder, Symbol
from typing import Tuple


class HuffmanDecodingException(Exception):
    def __init__(self):
        super().__init__("Unable to decode sequence of bits.")


class HuffmanDecoder(Decoder):
    def __init__(self, tree: HuffmanTree):
        assert (
            tree.root is not None
        ), "Must have non-null root to perform Huffman decoding"
        self.root = tree.root

    def __call__(self, bits: bitarray, start: int = 0) -> Tuple[Symbol, int]:
        if start >= len(bits):
            return None
        pos = start
        node = self.root
        while not node.is_leaf_node():
            bit = bits[pos]
            node = node.left if bit == 0 else node.right
            pos += 1
        return node.symbol, pos
