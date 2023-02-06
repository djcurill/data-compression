from src.lossless.decoders.huffman_decoder import HuffmanDecoder
from src.core.dist import Dist
from src.core.tree import HuffmanTree
from unittest import TestCase
from bitarray import bitarray


class TestHuffmanDecoder(TestCase):
    def setUp(self) -> None:
        self.tree = HuffmanTree(Dist("AAABBC"))
        self.encoded_bits = bitarray("111010100")  #
        return super().setUp()

    def test_decode_symbol_at_start(self):
        decoder = HuffmanDecoder(tree=self.tree)
        symbol, pos = decoder(self.encoded_bits, start=0)
        assert symbol == "A"
        assert pos == 1

    def test_decode_symbol_specific_position(self):
        decoder = HuffmanDecoder(tree=self.tree)
        symbol, pos = decoder(self.encoded_bits, start=3)
        assert symbol == "B"
        assert pos == 5

    def test_decode_symbol_when_start_is_greater_than_length_of_bits(self):
        decoder = HuffmanDecoder(tree=self.tree)
        assert decoder(self.encoded_bits, start=99) is None
