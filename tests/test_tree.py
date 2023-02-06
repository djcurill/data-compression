from src.core.tree import HuffmanTree
from src.core.dist import Dist
from src.core.node import Node
from unittest import TestCase
from bitarray import bitarray


class TestHuffmanTree(TestCase):
    def test_empty_tree(self):
        tree = HuffmanTree(Dist())
        assert tree.root is None
        assert not tree.get_encoding_table()

    def test_simple_tree_depth(self):
        tree = HuffmanTree(Dist("A"))
        assert isinstance(tree.root, Node)
        assert tree.root.symbol == "A"
        assert tree.max_depth() == 0

    def test_tree_depth(self):
        tree = HuffmanTree(Dist("AABCA"))
        assert isinstance(tree.root, Node)
        assert tree.max_depth() == 2

    def test_complex_tree_depth(self):
        tree = HuffmanTree(Dist("ABCDAABACDAD"))
        assert tree.max_depth() == 3

    def test_get_encoding_table_with_simple_tree(self):
        tree = HuffmanTree(Dist("A"))
        table = tree.get_encoding_table()
        assert table["A"] == bitarray("0")

    def test_get_encoding_table_with_complex_tree(self):
        tree = HuffmanTree(Dist("ABCDAABACDAD"))
        table = tree.get_encoding_table()
        assert table["A"] == bitarray("0")
        assert table["B"] == bitarray("111")
        assert table["C"] == bitarray("110")
        assert table["D"] == bitarray("10")

    def test_get_encoding_table_with_empty_tree(self):
        tree = HuffmanTree(Dist())
        assert not tree.get_encoding_table()
