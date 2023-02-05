from bitarray import bitarray
from core.tree import HoffmanTree
from src.lossless.decoders.base_decoder import Decoder, Symbol
from src.core.dist import Dist
from typing import Tuple

class HuffmanDecoder(Decoder):

    def __init__(self, dist:Dist):
        self.tree = HoffmanTree(dist=dist)

    def __call__(self, bits:bitarray, start:int=0) -> Tuple[Symbol, int]:
        node = self.tree.root
        if node is None:
            raise ValueError()

        pos = start
        while not node.is_leaf_node() and pos < len(bits):
            bit = bits[pos]
            node = node.left if bit == 0 else node.right
            pos += 1
            if node is None:
                raise ValueError()
        return node.symbol, pos


