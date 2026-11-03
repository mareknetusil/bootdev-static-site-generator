from collections.abc import Callable

from textnode import TextNode, TextType
from htmlnode import LeafNode, ParentNode, HTMLNode
from markdown import (
    block_to_block_type,
    markdown_to_blocks,
    BlockType,
    text_to_textnodes,
)


def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(tag=None, value=text_node.text)
        case TextType.BOLD:
            return LeafNode(tag="b", value=text_node.text)
        case TextType.ITALIC:
            return LeafNode(tag="i", value=text_node.text)
        case TextType.CODE:
            return LeafNode(tag="code", value=text_node.text)
        case TextType.LINK:
            if text_node.url is None:
                raise ValueError("link node needs an url value!")
            return LeafNode(
                tag="a", value=text_node.text, props={"href": text_node.url}
            )
        case TextType.IMG:
            if text_node.url is None:
                raise ValueError("image node needs an url value!")
            return LeafNode(
                tag="img",
                value=None,
                props={"href": text_node.url, "alt": text_node.text},
            )

    raise TypeError("unknown text node!")


def markdown_to_html_node(markdown: str) -> ParentNode:
    html_nodes = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_block_type(block)
        try:
            node = TYPE_TRANSFORM_MAP[block_type](block)
        except KeyError:
            raise ValueError("Unknown block!")

        html_nodes.append(node)
    return ParentNode("div", html_nodes)


def text_block_to_html_node(text: str, node_type: BlockType | str) -> ParentNode:
    text = text.replace("\n", " ")
    text_nodes = text_to_textnodes(text)
    children = [text_node_to_html_node(node) for node in text_nodes]
    tag = TYPE_TAG_MAP[node_type] if isinstance(node_type, BlockType) else node_type
    return ParentNode(tag, children)


def paragraph_to_node(block: str) -> ParentNode:
    return text_block_to_html_node(block, BlockType.PARAGRAPH)


def quote_to_node(block: str) -> ParentNode:
    block = "\n".join(line.replace(">", "") for line in block.split("\n"))
    return text_block_to_html_node(block, BlockType.QUOTE)


def code_to_node(block: str) -> HTMLNode:
    block = block.replace("```\n", "").replace("```", "")
    return ParentNode(
        "pre",
        [LeafNode("code", block)]
    )


def heading_to_node(block: str) -> ParentNode:
    mark, heading = block.split(" ", maxsplit=1)
    tag = f"h{len(mark)}"
    return text_block_to_html_node(heading, tag)


def unordered_list_to_node(block: str) -> ParentNode:
    lines = (line[2:] for line in block.split("\n"))
    list_elems = [LeafNode("li", line) for line in lines]
    return ParentNode("ul", list_elems)


def ordered_list_to_node(block: str) -> ParentNode:
    lines = (
        line.replace(f"{n}.", "", count=1)
        for n, line in enumerate(block.split("\n"), start=1)
    )
    list_elems = [LeafNode("li", line) for line in lines]
    return ParentNode("ol", list_elems)


TYPE_TRANSFORM_MAP: dict[BlockType, Callable[[str], HTMLNode]] = {
    BlockType.PARAGRAPH: paragraph_to_node,
    BlockType.QUOTE: quote_to_node,
    BlockType.HEADING: heading_to_node,
    BlockType.CODE: code_to_node,
    BlockType.UNORDERED_LIST: unordered_list_to_node,
    BlockType.ORDERED_LIST: ordered_list_to_node,
}


TYPE_TAG_MAP = {
    BlockType.PARAGRAPH: "p",
    BlockType.QUOTE: "blockquote",
}
