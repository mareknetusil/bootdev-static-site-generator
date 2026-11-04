import os
import pathlib as pl
from transform import markdown_to_html_node


def extract_title(markdown: str) -> str:
    try:
        title = next(filter(lambda line: line.startswith("# "), markdown.split("\n")))
    except StopIteration as e:
        raise ValueError("Can't extract title!") from e

    return title[2:]


def generate_page(
    from_path: pl.Path, template_path: pl.Path, dest_path: pl.Path, basepath: str
) -> None:
    print(f"Generating page from {from_path} to {dest_path} using {template_path}.")
    with open(from_path, "r") as f:
        content = f.read()
    with open(template_path, "r") as f:
        template = f.read()
    html_node = markdown_to_html_node(content)
    html = html_node.to_html()
    title = extract_title(content)
    webpage = template \
            .replace("{{ Title }}", title) \
            .replace("{{ Content }}", html) \
            .replace('href="/', f'href="{basepath}"') \
            .replace('src="/', f'src="{basepath}"')

    os.makedirs(dest_path.parent, exist_ok=True)
    with open(dest_path, "w") as f:
        f.write(webpage)


def generate_page_recursively(
    content_dir: pl.Path, template_path: pl.Path, dest_dir_path: pl.Path, basepath: str
) -> None:
    for dirname, _, files in content_dir.walk():
        if not files:
            continue
        rel_path = dirname.relative_to(content_dir)
        dest_dir = dest_dir_path / rel_path
        for file in files:
            generate_page(
                dirname / file,
                template_path,
                dest_dir / (file.strip(".md") + ".html"),
                basepath,
            )


if __name__ == "__main__":
    generate_page_recursively(
        pl.Path("content"), pl.Path("template.html"), pl.Path("public")
    )
