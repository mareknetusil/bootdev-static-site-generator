import logging
import pathlib as pl
import shutil
import sys

from webpage import generate_page_recursively

log = logging.getLogger()


def copy_directory(source: pl.Path, target: pl.Path) -> None:
    try:
        shutil.rmtree(target)
        shutil.copytree(source, target)
    except shutil.Error as e:
        log.critical(f"Failed to copy the source to target: {e}")


def main():
    try:
        basepath = sys.argv[1]
    except IndexError:
        basepath = "/"
    docs = pl.Path("docs")
    docs.mkdir(exist_ok=True)
    copy_directory(pl.Path("static"), docs)
    generate_page_recursively(
        pl.Path("content"),
        pl.Path("template.html"),
        docs,
        basepath
    )


if __name__ == "__main__":
    main()
