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

        return "".join(f" {key}=\"{value}\"" for key, value in self.props.items())
