"""
Note: You will catch a error if run directly a module which use the relative import.
- https://zhiqiang.org/coding/python-path-faq.html
- run tests: python -m unittest hyperlink-enrichment\\tests\\test_helpers.py
"""

import unittest
from ..src.helpers import ReadonlyNavigableDict

class ReadonlyNavigableDictTestCase(unittest.TestCase):

    def setUp(self):
        self.rn_dict = ReadonlyNavigableDict(
            dict([(11, "tom"), (88, "jack"), (10, "pony"), (1, "jerry")])
        )

    def test_floor_key(self):
        self.assertEqual(self.rn_dict.floor_key(100), 88)
        self.assertEqual(self.rn_dict.floor_key(10), 10)
        self.assertEqual(self.rn_dict.floor_key(5), 1)
        self.assertEqual(self.rn_dict.floor_key(1), 1)
        self.assertIsNone(self.rn_dict.floor_key(-5))

    def test_ceiling_key(self):
        self.assertIsNone(self.rn_dict.ceiling_key(100))
        self.assertEqual(self.rn_dict.ceiling_key(10), 10)
        self.assertEqual(self.rn_dict.ceiling_key(5), 10)
        self.assertEqual(self.rn_dict.ceiling_key(1), 1)
        self.assertEqual(self.rn_dict.ceiling_key(-5), 1)

    def test_floor_item(self): 
        self.assertEqual(self.rn_dict.floor_item(100), (88, "jack"))
        self.assertEqual(self.rn_dict.floor_item(10), (10, "pony"))
        self.assertEqual(self.rn_dict.floor_item(5), (1, "jerry"))
        self.assertEqual(self.rn_dict.floor_item(1), (1, "jerry"))
        self.assertIsNone(self.rn_dict.floor_item(-5))

    def test_ceiling_item(self):
        self.assertIsNone(self.rn_dict.ceiling_item(100))
        self.assertEqual(self.rn_dict.ceiling_item(10), (10, "pony"))
        self.assertEqual(self.rn_dict.ceiling_item(5), (10, "pony"))
        self.assertEqual(self.rn_dict.ceiling_item(1), (1, "jerry"))
        self.assertEqual(self.rn_dict.ceiling_item(-5), (1, "jerry"))