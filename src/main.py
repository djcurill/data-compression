from src.lossless.encoders.hoffman_encoder import HuffmanEncoder
from src.lossless.decoders.huffman_decoder import HuffmanDecoder
from src.core.dist import Dist
from src.core.tree import HoffmanTree
from src.compress import compress_bytes
from src.decompress import decompress
from src.utils import generate_random_data

data = generate_random_data(10000, p=0.1)
original_bytes = bytes(data)
dist = Dist(data)
tree = HoffmanTree(dist)
encoder = HuffmanEncoder(tree=tree)
decoder = HuffmanDecoder(tree=tree)
compressed_bits = compress_bytes(data, encoder)

decompressed_data = decompress(compressed_bits, decoder)
size_before = len(data) * 8
print(f"Size before compression (number of bits): {size_before}")

size_after = len(compressed_bits)
print(f"Size after compression (number of bits): {size_after}")

percent_compression = (1 - (size_after / size_before)) * 100
print(f"Percent compression: {percent_compression:.2f}")

if data == decompressed_data:
    print("Success: Decompression returned origin result")
else:
    print("Error: Original bytes do not equal decompressed bytes")

