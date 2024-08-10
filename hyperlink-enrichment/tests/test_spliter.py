import sideeffects
import unittest
import splitter


class TestSplitter(unittest.TestCase):
    def test_find_doc_meta(self):
        self.assertEqual(
            splitter.find("公司法", 2012),
            splitter.DocMeta("中华人民共和国公司法", "公司法", 2011),
        )
        self.assertEqual(
            splitter.find("公司法(2023修正)", 2023),
            splitter.DocMeta("中华人民共和国公司法(2023修正)", "公司法", 2023),
        )
        self.assertEqual(
            splitter.find("公司法(2019修正)", 2019),
            splitter.DocMeta("中华人民共和国公司法(2019修正)", "公司法", 2019),
        )
        self.assertEqual(
            splitter.find("公司法", 2008),
            splitter.DocMeta("中华人民共和国公司法(2008修正)", "公司法", 2008),
        )
        self.assertEqual(
            splitter.find("中华人民共和国公司法", 2008),
            splitter.DocMeta("中华人民共和国公司法(2008修正)", "公司法", 2008),
        )
        self.assertEqual(
            splitter.find("中华人民共和国公司法(2019修正)", 2024),
            splitter.DocMeta("中华人民共和国公司法(2019修正)", "公司法", 2019),
        )


if __name__ == "__main__":
    unittest.main()
