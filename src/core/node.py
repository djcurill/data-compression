from dataclasses import dataclass
from typing import Union

Symbol = Union[str, int]


@dataclass
class Node:
    count: int
    symbol: Symbol
    left = None
    right = None

    def is_leaf_node(self) -> bool:
        return self.left is None and self.right is None

    def __lt__(self, other) -> bool:
        if other.__class__ is self.__class__:
            return self.count < other.count

    def __gt__(self, other) -> bool:
        if other.__class__ is self.__class__:
            return self.count > other.count

    def __eq__(self, other) -> bool:
        if other.__class__ is self.__class__:
            return self.count == other.count

    def __le__(self, other) -> bool:
        if other.__class__ is self.__class__:
            return self.count <= other.count

    def __ge__(self, other) -> bool:
        if other.__class__ is self.__class__:
            return self.count >= other.count
