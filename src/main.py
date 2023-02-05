from collections import defaultdict, Counter
from dataclasses import dataclass
from typing import Union
from typing import List
from abc import ABC, abstractmethod
from bitarray import bitarray

class Node:
    def __init__(self, symbol:int, count:int):
        self.symbol = symbol
        self.count = count
        self.left = None
        self.right = None

    def __repr__(self) -> str:
        return f"Node(symbol='{self.symbol}', count={self.count})"

    def is_leaf_node(self) -> bool:
        return self.left is None and self.right is None


class Dist(Counter):
    """Store distribution of input data"""


class HoffmanTree:

    def __init__(self, dist:dict):
        self.encoding_table = {}
        self.root = self.build(dist)
        self.encoding_table = self.create_encoding_table(self.root)

    @staticmethod
    def build(dist:dict):
        if not dist:
            raise ValueError("Cannot create tree with empty distribution")
        list_of_nodes = [Node(symbol, count) for symbol,count in dist.items()]
        while len(list_of_nodes) > 1:
            list_of_nodes = sorted(list_of_nodes, key=lambda x: x.count, reverse=True)
            n1 = list_of_nodes.pop()
            n2 = list_of_nodes.pop()
            merged_node = Node(symbol=".", count=n1.count + n2.count)
            merged_node.right = n1
            merged_node.left = n2
            list_of_nodes.append(merged_node)
        return list_of_nodes.pop()

    @staticmethod
    def create_encoding_table(tree:Node):
        encoding_table = {}
        def _dfs(tree:Node, code:str) -> None:
            if tree.is_leaf_node():
                encoding_table[tree.symbol] = code
                return
            if tree.left is not None:
                _dfs(tree.left, code + "0")
            if tree.right is not None:
                _dfs(tree.right, code + "1")
        _dfs(tree, code="")
        return encoding_table



    @abstractmethod
    def decode(self, bits: bitarray) -> Symbol:
        pass

