import unittest

from textnode import TextNode, TextType
from markdown import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
    markdown_to_blocks,
    block_to_block_type,
    BlockType,
    ParsedImage,
    ParsedURL,
)


class TestMarkdown(unittest.TestCase):
    def test_split_nodes_delimiter(self):
        node = TextNode("Hello, _World_", TextType.TEXT)
        self.assertEqual(
            split_nodes_delimiter([node], "_", TextType.ITALIC),
            [
                TextNode("Hello, ", TextType.TEXT),
                TextNode("World", TextType.ITALIC),
            ],
        )

    def test_split_nodes_delimiter_empty(self):
        self.assertEqual(split_nodes_delimiter([], "_", TextType.ITALIC), [])

    def test_split_nodes_delimiter_unclosed(self):
        node = TextNode("Hello, _World", TextType.TEXT)
        self.assertRaises(
            ValueError, lambda: split_nodes_delimiter([node], "_", TextType.ITALIC)
        )

    def test_split_nodes_delimiter_begins(self):
        node = TextNode("_Hello_, World", TextType.TEXT)
        self.assertEqual(
            split_nodes_delimiter([node], "_", TextType.ITALIC),
            [
                TextNode("Hello", TextType.ITALIC),
                TextNode(", World", TextType.TEXT),
            ],
        )

    def test_split_nodes_delimiter_leaves_others(self):
        node1 = TextNode("Hello", TextType.ITALIC)
        node2 = TextNode(", World", TextType.TEXT)
        self.assertEqual(
            split_nodes_delimiter([node1, node2], "_", TextType.ITALIC), [node1, node2]
        )

    def test_extract_markdown_images(self):
        first = "![first](http://fake.com/first)"
        second = "![second](http://fake.com/second)"
        text = f"Look at {first}. Then at {second}."
        first_pos = text.find(first)
        second_pos = text.find(second)
        self.assertEqual(
            extract_markdown_images(text),
            [
                ParsedImage(
                    "first",
                    "http://fake.com/first",
                    (first_pos, first_pos + len(first)),
                ),
                ParsedImage(
                    "second",
                    "http://fake.com/second",
                    (second_pos, second_pos + len(second)),
                ),
            ],
        )

    def test_extract_markdown_images_empty(self):
        self.assertEqual(extract_markdown_images("Hello, World."), [])

    def test_extract_markdown_links(self):
        first = "[first](http://fake.com/first)"
        second = "[second](http://fake.com/second)"
        text = f"Look at {first}. Then at {second}."
        first_pos = text.find(first)
        second_pos = text.find(second)
        self.assertEqual(
            extract_markdown_links(text),
            [
                ParsedURL(
                    "first",
                    "http://fake.com/first",
                    (first_pos, first_pos + len(first)),
                ),
                ParsedURL(
                    "second",
                    "http://fake.com/second",
                    (second_pos, second_pos + len(second)),
                ),
            ],
        )

    def text_extract_markdown_links_empty(self):
        self.assertEqual(extract_markdown_links("Hello, World."), [])

    def test_split_nodes_images(self):
        nodes = [
            TextNode(
                "Look at ![first](http://fake.com/first). Then at ![second](http://fake.com/second).",
                TextType.TEXT,
            )
        ]
        self.assertEqual(
            split_nodes_image(nodes),
            [
                TextNode("Look at ", TextType.TEXT),
                TextNode("first", TextType.IMG, "http://fake.com/first"),
                TextNode(". Then at ", TextType.TEXT),
                TextNode("second", TextType.IMG, "http://fake.com/second"),
                TextNode(".", TextType.TEXT),
            ],
        )

    def test_split_nodes_links(self):
        nodes = [
            TextNode(
                "Look at [first](http://fake.com/first). Then at [second](http://fake.com/second).",
                TextType.TEXT,
            )
        ]
        self.assertEqual(
            split_nodes_link(nodes),
            [
                TextNode("Look at ", TextType.TEXT),
                TextNode("first", TextType.LINK, "http://fake.com/first"),
                TextNode(". Then at ", TextType.TEXT),
                TextNode("second", TextType.LINK, "http://fake.com/second"),
                TextNode(".", TextType.TEXT),
            ],
        )

    def test_split_nodes_links_does_not_touch_images(self):
        text = "Look at ![first](http://fake.com/first). Then at ![second](http://fake.com/second)."
        nodes = [TextNode(text, TextType.TEXT)]
        self.assertEqual(
            split_nodes_link(nodes),
            [TextNode(text, TextType.TEXT)],
        )

    def test_text_to_textnodes(self):
        text = (
            "**Look** at _picture_ ![first](http://fake.com/first). "
            "Then at _link_ [second](http://fake.com/second)."
        )
        self.assertEqual(
            text_to_textnodes(text),
            [
                TextNode("Look", TextType.BOLD),
                TextNode(" at ", TextType.TEXT),
                TextNode("picture", TextType.ITALIC),
                TextNode(" ", TextType.TEXT),
                TextNode("first", TextType.IMG, "http://fake.com/first"),
                TextNode(". Then at ", TextType.TEXT),
                TextNode("link", TextType.ITALIC),
                TextNode(" ", TextType.TEXT),
                TextNode("second", TextType.LINK, "http://fake.com/second"),
                TextNode(".", TextType.TEXT),
            ],
        )

    def test_markdown_to_blocks(self):
        text = """
# Heading

First paragraph of the text. Followed by some list:

- first item
- second item
- third item

And some conclusion.
"""
        self.assertEqual(
            markdown_to_blocks(text),
            [
                "# Heading",
                "First paragraph of the text. Followed by some list:",
                "- first item\n- second item\n- third item",
                "And some conclusion.",
            ],
        )

    def test_block_to_block_type_paragraph(self):
        text = "#This is some paragraph. ``"
        self.assertEqual(block_to_block_type(text), BlockType.PARAGRAPH)

    def test_block_to_block_type_heading(self):
        text = "## This is heading"
        self.assertEqual(block_to_block_type(text), BlockType.HEADING)

    def test_block_to_block_type_code(self):
        text = """
```
x = 1 + 3
```"""
        self.assertEqual(block_to_block_type(text.strip()), BlockType.CODE)

    def test_block_to_block_type_quote(self):
        text = """
> Quotes are useless...
> ... Some dude probably"""
        self.assertEqual(block_to_block_type(text.strip()), BlockType.QUOTE)

    def test_block_to_block_type_unordered_list(self):
        text = """
- first item
- second item"""
        self.assertEqual(block_to_block_type(text.strip()), BlockType.UNORDERED_LIST)

    def test_block_to_block_type_ordered_list(self):
        text = """
1. first item
2. second item"""
        self.assertEqual(block_to_block_type(text.strip()), BlockType.ORDERED_LIST)

    def test_block_to_block_type_ordered_list_wrong(self):
        text = """
2. first item
3. second item"""
        self.assertEqual(block_to_block_type(text.strip()), BlockType.PARAGRAPH)


if __name__ == "__main__":
    unittest.main()
