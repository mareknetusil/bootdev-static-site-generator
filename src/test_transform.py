import unittest

from textnode import TextNode, TextType
from transform import text_node_to_html_node, markdown_to_html_node


class TestTransform(unittest.TestCase):
    def test_text_to_html(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_link_to_html(self):
        node = TextNode("Google", TextType.LINK, url="http://www.google.com")
        html = text_node_to_html_node(node).to_html()
        self.assertEqual(html, '<a href="http://www.google.com">Google</a>')

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )


    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        expected_html = "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>"
        self.assertEqual(html, expected_html)

    def test_heading(self):
        md = """
# Main title

Some text

## Chapter 1

another text
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Main title</h1><p>Some text</p><h2>Chapter 1</h2><p>another text</p></div>"
        )


if __name__ == "__main__":
    unittest.main()
