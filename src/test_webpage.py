import unittest

from webpage import extract_title


class WebPageTest(unittest.TestCase):
    def test_extract_title(self):
        self.assertEqual(extract_title("# Title"), "Title")

    def test_extract_title_error(self):
        self.assertRaises(ValueError, lambda: extract_title("Title"))


if __name__ == "__main__":
    unittest.main()
