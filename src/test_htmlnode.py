import unittest
from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_repr(self):
        tag = "bar"
        value = "foo"
        node = HTMLNode(tag, value)
        output = str(node)
        self.assertTrue("HTMLNode" in output)
        self.assertTrue(tag in output)
        self.assertTrue(value in output)

    def test_defaults(self):
        node = HTMLNode()
        self.assertEqual(node.tag, None)
        self.assertEqual(node.value, None)
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)

    def test_empty_props(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")

    def test_props(self):
        node = HTMLNode(props={"href": "foo", "alt": "bar"})
        props_html = node.props_to_html()
        self.assertTrue(props_html.startswith(" "))
        self.assertTrue("href=\"foo\"" in props_html)
        self.assertTrue("alt=\"bar\"" in props_html)


if __name__ == "__main__":
    unittest.main()
