from src.core.dist import Dist
from unittest import TestCase

class TestDist(TestCase):

    def test_dist(self):
        # Test simplie initialization
        d = Dist("a" * 4)
        self.assertEqual(d['a'], 1.0) # 100% are a's

        # Test multi variable list
        d = Dist([1,1,3,4,1,2,2,1,2,3])
        self.assertDictEqual(d,{1:0.4, 3:0.2, 4:0.1, 2:0.3})

        # Test empty condition
        d = Dist()
        self.assertFalse(d)

    