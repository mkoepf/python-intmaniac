import unittest

from intmaniac.tools import deep_merge


class TestDeepMerge(unittest.TestCase):

    def test_basic_function(self):
        d0 = {1: 2}
        d1 = {2: 3}
        result = {1: 2, 2: 3}
        self.assertDictEqual(deep_merge(d0, d1), result)

    def test_key_priority(self):
        d0 = {1: 2, 2: [1, 2, 3]}
        d1 = {1: 3, 2: 3}
        result = {1: 3, 2: 3}
        self.assertDictEqual(deep_merge(d0, d1), result)

    def test_deep_merging(self):
        d0 = {1: {2: 3, 3: 4}, 7: 8}
        d1 = {1: {4: 5, 3: 3}, 8: 9}
        result = {1: {2: 3, 3: 3, 4: 5}, 7: 8, 8: 9}
        self.assertDictEqual(deep_merge(d0, d1), result)
