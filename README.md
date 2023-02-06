# Problem Statement

Design an algorithm that will compress a given data buffer of bytes. Please describe your design and submit an implementation in Python.
Your submission will be judged based on

- The number of bytes your output uses if saved to file
- Run time
- Scalability
- Maintainability
- Testability

**Assumptions**

1. data is an array of bytes. Each byte will contain a number from 0 to 127 (0x00 to 0x7F). It is common for the data in the buffer to have the same value repeated in the series.
2. The compressed data will need to be decompressable. Please ensure that your algorithm allows for a decompression algorithm to return the buffer to its previous form.

**Example**

```python
data = bytes([0x03, 0x74, 0x04, 0x04, 0x04, 0x35, 0x35, 0x64,
0x64, 0x64, 0x64, 0x00, 0x00, 0x00, 0x00, 0x00,
0x56, 0x45, 0x56, 0x56, 0x56, 0x09, 0x09, 0x09])
compressed_bytes = byte_compress(data)
```

## Algorithm Design

There are two important properties that can be leveraged to reduce the size of data:

1. The sequence of bytes consist of numbers that range from 0 - 127.
2. Numbers tend to repeat themselves which suggests the distribution of integers will likely be skewed (i.e. not uniform).

In addition, the compression algorithm must be *lossless* so that the data can be perfectly decompressed.

Two popular algorithms I found that could be used to compress the data in a lossless fashion. Each will have their tradeoffs.

1. Fixed length encoding
2. Huffman encoding

### Choosing an Algorithm (evaluating tradeoffs)

#### Fixed Length Enconding

**Pros**

- Simple to implement
- Performs better with greater entropy (i.e. more random distribution)

**Cons**

- Performs much worse given a skewed distribution

#### Huffman Encoding

**Pros**

- Performs better given repeating values
- Will perform similar to fixed encoding given large input sample size (will derive fixed encoding as n increases)

**Cons**

- More complex to implement
- Performance will level out as sample size becomes large enough to include the full population (0-127)

The huffman enconding technique offers more flexibility and will likely outperform the Fixed length encoding method should the data be much more likely to be skewed. This algorithm will not perform well if the distribution of data turns out to be uniform (i.e. a high degree of entropy).

## How Huffman Enconding Works

Huffman encoding takes advantage of repeating values. Given a sequence of bytes, any bytes that occur more frequently than others, will be assigned an encoding that uses a smaller number of bits. More rare occurences will use more bits, meaning they take up more space but occur less frequently.

This algorithm can be broken up into steps:

**Step 1**: Compute the probability distribution of the data.

Source Code: [src.core.dist.py](https://github.com/djcurill/data-compression/blob/main/src/core/dist.py)

Example:

```python
>>> from src.core.dist import Dist
>>> Dist([1,1,1,2,3])
{1: 0.6, 2: 0.2, 3: 0.2}
```

**Step 2**: Represent each item in the distribution as a node

Source code: [src/core/node.py](https://github.com/djcurill/data-compression/blob/main/src/core/node.py)

Nodes will be used to eventually create a tree structure. The following pseudcode describes the structure of a Node:

```python
class Node:
    count:float            # How often a symbol occurs (i.e. the probability)
    symbol:Union[str,int]  # String representation of the symbol (in our case, this would be the byte)
    left:Node              # Left child node
    right:Node             # Right child node
```

Example:

```python
>>> from src.core.dist import Dist
>>> Dist([1,1,1,2,3])
{1: 0.6, 2: 0.2, 3: 0.2}
>>> from src.core.node import Node
>>> Node(count=0.6, symbol=0x01)
Node(count=0.6, symbol=1)
```

---
**Step 3**: Create a Huffman Tree

Source code: [src/core/tree.py](https://github.com/djcurill/data-compression/blob/main/src/core/tree.py)

Create a huffman given a distribution. This can be broken into steps:

1. Create a list of nodes from a distrbution
2. Iterate over the list of nodes until eventually only the root remains
3. In each iteration, take the two nodes with smallest `count` values and merge them.
4. Append the merged node back into the list.
5. Repeat
6. When only one node remains, return the root node. This is the Huffman Tree.

---
**Step 4**: Create an encoding table

Source code: [src/core/tree.py](https://github.com/djcurill/data-compression/blob/main/src/core/tree.py)

An encoding table will map a `symbol` to its bit representation. In python, the [bitarray library](https://pypi.org/project/bitarray/) provides helper methods to represent objects as bits. The bitarray representation of a symbol is determined by the number of `lefts` and `rights` taken to navigate from the `root` node to a leaf node in a Huffman Tree. This algorithm ensures that each symbol has a unique prefix so that there are no issues when decoding.

To create an encoding table from a Huffman tree, you take the all the leaf nodes and transform it into a dictionary that maps `symbol` to `bits`. This can be done using a simple depth first search algorithm. Source code has been copy and pasted below:

```python
def get_encoding_table(self) -> Dict[str, bitarray]:
    encoding_table = {}

    def _dfs(tree:Node, code:str) -> None:
        if tree.is_leaf_node():
            # Must handle edge case where tree is only root node
            code = code if code else "0"
            encoding_table[tree.symbol] = bitarray(code)
            return
        if tree.left is not None:
            _dfs(tree.left, code + "0")
        if tree.right is not None:
            _dfs(tree.right, code + "1")

    if self.root is not None:
        _dfs(self.root, code="")
    return encoding_table
```

---
**Step 5**: Encoding Algorithm

Source code: [src/lossless/encoders/huffman_encoder.py](https://github.com/djcurill/data-compression/blob/main/src/lossless/encoders/huffman_encoder.py)

This algorithm is really simple. Just take a symbol and map it to its `bitarray` representation.

Example:

```python
>>> from src.lossless.encoders.huffman_encoder import HuffmanEncoder
>>> from src.core.tree import HuffmanTree
>>> from src.core.dist import Dist
>>> dist = Dist([1,1,1,1,2,2,2,3])
>>> tree = HuffmanTree(dist)
>>> encoder = HuffmanEncoder(tree)
>>> encoder(1)
bitarray('1')
```

---
**Step 6:** Decoding Algorithm

Source code: [src/lossless/decoders/huffman_decoder.py](https://github.com/djcurill/data-compression/blob/main/src/lossless/decoders/huffman_decoder.py)

Decoding a sequence of bits is quite elegant with a Huffman Tree. Given a sequence of bits, you iteratively traverse a bit sequence and navigate the Huffman Tree until a leaf node has been reached. If the bit is `0` go the left child node. If the bit is `1`, go to the right child node. Each `symbol -> bitarray` mapping is guaranteed to be unique since the tree was constructed using the optimal merge pattern. That means no two symbols can have the same prefix of bits. Below is the implementation of the decoding algorithm:

```python
class HuffmanDecoder(Decoder):

    def __init__(self, tree:HuffmanTree):
        assert tree.root is not None, "Must have non-null root to perform Huffman decoding"
        self.root = tree.root

    def __call__(self, bits:bitarray, start:int=0) -> Tuple[Symbol, int]:
        if start >= len(bits):
            return None
        pos = start
        node = self.root
        while not node.is_leaf_node():
            bit = bits[pos]
            node = node.left if bit == 0 else node.right
            pos += 1
        return node.symbol, pos
```

---

**Step 7:** Putting it all together

See [main.py](https://github.com/djcurill/data-compression/blob/main/src/main.py) for the full implementation.

The compression performance will be determined by computing the number of bytes before and after compression and then calculating the compression ratio.

The size after compression is the addition of:

1. The number of bytes to represent compressed data and,
2. The number of bytes to represent the encoding table

The compression ratio is calculated by:
```python
(1 - (after / before)) * 100
```

## Running the algorithm

This environment uses Python 3.9.

To setup the environment run the following commands:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Ensure all tests are passing:

```bash
make test
```

To run the code using the example provided in the problem statement:

```bash
make run-example
```

To run a custom experiment:

```bash
make run-experiment SIZE=100 PROB=0.9
```

`SIZE` will control the number of bytes to be compressed and `PROB` is the probability of a byte repeating itself. The higher `PROB` is, the more skewed the distribution.

## Learning & Limitations

- The performance of the algorithm will greatly slow down with much higher numbers (~1000000). Bottleneck appears to be the tree traversing when decoding compressed bits.
- Compression performs very well with large input size. This is likely because size of python integers from 0-127 are quite large.
