from src.lossless.encoders.huffman_encoder import HuffmanEncoder
from src.lossless.decoders.huffman_decoder import HuffmanDecoder
from src.core.dist import Dist
from src.core.tree import HuffmanTree
from src.compress import compress_bytes
from src.decompress import decompress
from src.utils import generate_random_data
from argparse import ArgumentParser
import sys
import ast


def huffman_lossless(data) -> None:
    # Encode data
    dist = Dist(data)
    tree = HuffmanTree(dist)
    encoder = HuffmanEncoder(tree=tree)
    decoder = HuffmanDecoder(tree=tree)
    compressed_bits = compress_bytes(data, encoder)

    # Decode data
    decompressed_data = decompress(compressed_bits, decoder)

    # Evaluate before and after compression stats
    size_before = sum(map(lambda x: sys.getsizeof(bytes(x)), data))
    print(f"Size before compression (number of bits): {size_before}")

    size_of_compressed_data = sys.getsizeof(compressed_bits.tobytes())
    size_of_encoding_table = sys.getsizeof(tree.get_encoding_table())
    size_after = size_of_compressed_data + size_of_encoding_table
    print(f"Size after compression (number of bits): {size_after}")

    percent_compression = (1 - (size_after / size_before)) * 100
    print(f"Percent compression: {percent_compression:.2f}")

    # Determine if compression was lossless
    if data == decompressed_data:
        print("Success: Decompression returned origin result")
    else:
        print("Error: Original bytes do not equal decompressed bytes")


if __name__ == "__main__":
    parser = ArgumentParser(
        prog="HuffmanCompression",
        description="Compress sequence of bytes using Huffman encoding",
    )
    parser.add_argument("--fixed", help="Run example using fixed dataset")
    parser.add_argument("-s", "--size", default=100)
    parser.add_argument(
        "-p",
        "--prob",
        default=0.9,
        help="probability of a value repeating itself. Higher prob mean greater skew",
    )
    args = parser.parse_args()

    if ast.literal_eval(args.fixed):
        print("here")
        data = [
            0x03,
            0x74,
            0x04,
            0x04,
            0x04,
            0x35,
            0x35,
            0x64,
            0x64,
            0x64,
            0x64,
            0x00,
            0x00,
            0x00,
            0x00,
            0x00,
            0x56,
            0x45,
            0x56,
            0x56,
            0x56,
            0x09,
            0x09,
            0x09,
        ]
    else:
        data = generate_random_data(int(args.size), float(args.prob))

    huffman_lossless(data)
