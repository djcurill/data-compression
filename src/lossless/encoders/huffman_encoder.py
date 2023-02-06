from src.lossless.encoders.base_encoder import Encoder, Symbol
from src.core.tree import HuffmanTree


class HuffmanEncodingException(Exception):
    def __init__(self, symbol: Symbol):
        message = f"Huffman Encoding Error: Unable to encode symbol: {symbol}"
        super().__init__(message)


class HuffmanEncoder(Encoder):
    def __init__(self, tree: HuffmanTree):
        self.tree = tree
        self.encoding_table = tree.get_encoding_table()

    def __call__(self, symbol: Symbol) -> str:
        try:
            return self.encoding_table[symbol]
        except KeyError:
            raise HuffmanEncodingException(symbol=symbol)
