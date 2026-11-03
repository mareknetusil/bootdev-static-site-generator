import dataclasses as dc
import enum
import itertools as it
import re

from textnode import TextNode, TextType


class BlockType(enum.Enum):
    PARAGRAPH = enum.auto()
    HEADING = enum.auto()
    CODE = enum.auto()
    QUOTE = enum.auto()
    UNORDERED_LIST = enum.auto()
    ORDERED_LIST = enum.auto()


@dc.dataclass
class ParsedImage:
    alt: str
    url: str
    pos: tuple[int, int]


@dc.dataclass
class ParsedURL:
    anchor_text: str
    url: str
    pos: tuple[int, int]


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
) -> list[TextNode]:
    new_list = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_list.append(node)
            continue
        parts = node.text.split(delimiter)
        if len(parts) % 2 == 0:
            raise ValueError(
                f"text node has an unmatched delimiter. del: {delimiter}, text: {node.text}"
            )
        for target_type, part in zip(it.cycle((TextType.TEXT, text_type)), parts):
            if not part:
                continue
            new_node = TextNode(part, target_type)
            new_list.append(new_node)

    return new_list


def extract_markdown_images(text: str) -> list[ParsedImage]:
    matches = re.finditer(r"\!\[(.*?)\]\((.*?)\)", text)
    return [ParsedImage(*match.group(1, 2), match.span()) for match in matches]


def extract_markdown_links(text: str) -> list[ParsedURL]:
    matches = re.finditer(r"(?<!\!)\[(.*?)\]\((.*?)\)", text)
    return [ParsedURL(*match.group(1, 2), match.span()) for match in matches]


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_list = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_list.append(node)
            continue
        text = node.text
        img_matches = extract_markdown_images(text)
        last_pos = 0
        for img in img_matches:
            start, end = img.pos
            if start > last_pos:
                new_list.append(TextNode(text[last_pos:start], TextType.TEXT))
            new_list.append(TextNode(img.alt, TextType.IMG, img.url))
            last_pos = end
        if last_pos < len(text):
            new_list.append(TextNode(text[last_pos:], TextType.TEXT))
    return new_list


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_list = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_list.append(node)
            continue
        text = node.text
        link_matches = extract_markdown_links(text)
        last_pos = 0
        for link in link_matches:
            start, end = link.pos
            if start > last_pos:
                new_list.append(TextNode(text[last_pos:start], TextType.TEXT))
            new_list.append(TextNode(link.anchor_text, TextType.LINK, link.url))
            last_pos = end
        if last_pos < len(text):
            new_list.append(TextNode(text[last_pos:], TextType.TEXT))
    return new_list


def text_to_textnodes(text: str) -> list[TextNode]:
    nodes = [TextNode(text, TextType.TEXT)]
    for delim, node_type in FORMAT_DICT.items():
        nodes = split_nodes_delimiter(nodes, delim, node_type)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes


FORMAT_DICT = {
    "**": TextType.BOLD,
    "_": TextType.ITALIC,
    "`": TextType.CODE,
}


def markdown_to_blocks(text: str) -> list[str]:
    return [line for raw_line in text.split("\n\n") if (line := raw_line.strip())]


def block_to_block_type(block: str) -> BlockType:
    if re.match(r"^#{1,6} .*", block):
        return BlockType.HEADING

    if block.startswith("```\n") and block.endswith("```"):
        return BlockType.CODE

    lines = block.split("\n")
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE

    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST

    if all(line.startswith(f"{n}.") for n, line in enumerate(lines, start=1)):
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH
