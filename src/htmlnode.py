import dataclasses as dc


@dc.dataclass(frozen=True, slots=True)
class HTMLNode:
    tag: str | None = None
    value: str | None = None
    children: list["HTMLNode"] | None = None
    props: dict[str, str] | None = None

    def to_html(self) -> str:
        raise NotImplementedError

    def props_to_html(self) -> str:
        if self.props is None:
            return ""

        return "".join(f' {key}="{value}"' for key, value in self.props.items())


class LeafNode(HTMLNode):
    def __init__(
        self, tag: str | None, value: str | None, props: dict[str, str] | None = None
    ):
        super().__init__(tag=tag, value=value, props=props)

    def to_html(self) -> str:
        if self.tag is None:
            return self.value or ""

        if self.value is None:
            return f"<{self.tag}{self.props_to_html()}/>"
        else:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    def __init__(
        self, tag: str, children: list[HTMLNode], props: dict[str, str] | None = None
    ):
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self) -> str:
        if self.tag is None:
            raise ValueError("all parent nodes must have a tag!")

        if self.children is None:
            raise ValueError("all parent nodes must have children!")

        children_html = "".join(node.to_html() for node in self.children)
        return f"<{self.tag}>{children_html}</{self.tag}>"
