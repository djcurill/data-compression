from typing import Iterable, Dict
from src.core.node import Node
from src.core.dist import Dist
from bitarray import bitarray


class HuffmanTree:
    def __init__(self, dist: Dist):
        self.root = self.create_tree(dist)
        self._encoding_table = {}

    @staticmethod
    def create_tree(dist: Iterable) -> Node:
        if not dist:
            return
        list_of_nodes = [
            Node(symbol=symbol, count=count) for symbol, count in dist.items()
        ]
        while len(list_of_nodes) > 1:
            list_of_nodes = sorted(list_of_nodes, reverse=True)
            n1 = list_of_nodes.pop()
            n2 = list_of_nodes.pop()
            merged_node = Node(symbol=".", count=n1.count + n2.count)
            merged_node.left = n1
            merged_node.right = n2
            list_of_nodes.append(merged_node)
        return list_of_nodes.pop()

    def get_encoding_table(self) -> Dict[str, bitarray]:
        encoding_table = {}

        def _dfs(tree: Node, code: str) -> None:
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

    def max_depth(self) -> int:
        global max_depth
        max_depth = 0

        def _dfs(tree: Node, level: int) -> None:
            if tree.is_leaf_node():
                global max_depth
                max_depth = max(level, max_depth)
                return
            if tree.left is not None:
                _dfs(tree.left, level + 1)
            if tree.right is not None:
                _dfs(tree.right, level + 1)

        if self.root is not None:
            _dfs(self.root, 0)
        return max_depth
