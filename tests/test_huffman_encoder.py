from bitarray import bitarray
from src.core.dist import Dist
from src.lossless.encoders.hoffman_encoder import HuffmanEncoder, HuffmanEncodingException
from unittest import TestCase

class TestHuffmanEncoder(TestCase):

    def test_encode_symbol(self):
        dist = Dist("AABCAACBABB")
        encoder = HuffmanEncoder(dist=dist)
        assert encoder("A") == bitarray("0")
        assert encoder("B") in [bitarray("10"), bitarray("11")]
        assert encoder("C") in [bitarray("10"), bitarray("11")]

    def test_encoder_raises_error_when_symbol_not_found(self):
        dist = Dist("AABCAACBABB")
        encoder = HuffmanEncoder(dist=dist)
        with self.assertRaises(HuffmanEncodingException):
            encoder("Z")