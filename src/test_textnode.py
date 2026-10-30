import unittest
from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_noneq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is ANOTHER text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_default_url(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node.url, None)


if __name__ == "__main__":
    unittest.main()
