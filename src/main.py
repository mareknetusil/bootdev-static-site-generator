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
    copy_directory(pl.Path("static"), pl.Path("public"))
    generate_page_recursively(
        pl.Path("content"),
        pl.Path("template.html"),
        pl.Path("public"),
    )


if __name__ == "__main__":
    main()
