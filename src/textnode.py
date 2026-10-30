import dataclasses as dc
from enum import StrEnum, auto

class TextType(StrEnum):
    BOLD = auto()
    ITALIC = auto()
    CODE = auto()
    LINK = auto()
    IMG = auto()


@dc.dataclass(frozen=True, slots=True)
class TextNode:
    text: str
    text_type: TextType
    url: str | None = None

    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type}, {self.url})"

