import unittest

import side_effects  # noqa: F401 - It's a side-effects module.
from extract_anchor import PairedKeyword as PKW
from extract_anchor import PairedKeywordExtractor


class PairedKeywordExtractorTestCase(unittest.TestCase):
    def test_single_pair(self):
        extractor = PairedKeywordExtractor((("<", ">"),))
        keywords = extractor.extract(
            "This is an example text <containing> some <keywords> within angle brackets."
        )
        self.assertEqual(
            keywords, [PKW("<containing>", 24, 36), PKW("<keywords>", 42, 52)]
        )

    def test_a_set_of_paris(self):
        extractor = PairedKeywordExtractor((("<", ">"), ("《", "》")))
        keywords = extractor.extract(
            "This is an <example text> containing some 《keywords》."
        )
        self.assertEqual(
            keywords, [PKW("<example text>", 11, 25), PKW("《keywords》", 42, 52)]
        )

    def test_pairs_nested(self):
        extractor = PairedKeywordExtractor((("<", ">"), ("《", "》")))
        keywords = extractor.extract(
            "This is an <example text> containing 《some <keywords>》."
        )
        child = PKW("<keywords>", 43, 53)
        parent = PKW("《some <keywords>》", 37, 54)
        child.parent = parent
        parent.add_child(child)
        self.assertEqual(keywords, [PKW("<example text>", 11, 25), parent, child])


def suite():
    """
    DeprecationWarning: unittest.makeSuite() is deprecated and will be removed in Python 3.13. Please use unittest.TestLoader.loadTestsFromTestCase() instead.
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(PairedKeywordExtractorTestCase))
    """
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(PairedKeywordExtractorTestCase)
    return suite


if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(suite())
