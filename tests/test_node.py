from src.core.node import Node
from unittest import TestCase


class TestNode(TestCase):
    def test_equals(self):
        a = Node(1, "a")
        b = Node(1, "a")
        c = Node(1, "b")
        self.assertEqual(a, b)
        self.assertEqual(a, c)

    def test_comparisons(self):
        one = Node(1, "one")
        two = Node(2, "two")
        self.assertTrue(one < two)
        self.assertTrue(two > one)
        self.assertTrue(one <= two)
        self.assertTrue(two >= one)

    def test_minimum(self):
        nodes = [Node(1, "one"), Node(2, "two"), Node(0, "zero")]
        self.assertEqual(min(nodes).count, 0)
