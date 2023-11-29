#!/usr/bin/env python

import os
import sys
from glob import glob
from pathlib import Path as P
from typing import Generator

import requests
import typer

TARGET = ".gitignore"
GITHUB_PROJECT = "https://github.com/bwagner/gitignore.git"

"""
Concatenates gitignore-snippets found in the local directory to form a target
.gitignore.
Optionally refreshes snippets listed in gitignore-snippets.txt beforehand by
downloading them.
gitignore-snippets.txt is passed via the command line.

To add a new snippet:
    - if it is maintained in a github repo:
        - find a url where the new snippet is maintained. Candidates:
          https://github.com/github/gitignore/tree/main/Global
        - append the url to gitignore-snippets.txt
        - run make_gitignore.py -u
    - if it is a file you plan to maintain locally:
      - make sure its name ends in .gitignore
      - add it to the repo
        - run make_gitignore.py


To remove a snippet:
    - remove the url from gitignore-snippets.txt
    - remove the local copy of the snippet (if it is maintained
      in the repo, git rm it)
    - run make_gitignore.py

TODO:
    - using pathlib.Path to wrangle urls because yarl doesn't
      work for python 3.12 currently, as it seems due to a
      dependency on multidict.
"""


def get_snippet_to_url(snippets: str) -> dict[str, str]:
    """
    Retrieves gitignore-snippets.txt file and returns a dictionary mapping
    the snippet to its originating url.
    """
    snippet_to_url = {}
    for line in read_file(snippets):
        url = line.strip()
        snippet_to_url[P(url).name] = url
    return snippet_to_url


def download_file(url: str, target: str) -> str:
    """
    Downloads a file from the url, saving it in local target.
    adapted from: https://stackoverflow.com/a/16696317
    """
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(target, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    return target


def read_file(file_path) -> Generator[str, None, None]:
    """
    Generator to read a file line by line.
    """
    with P(file_path).open() as file:
        yield from file


def get_snippets(snippets: str) -> None:
    """
    Downloads files listed in snippets.
    """
    with P(snippets).open() as f:
        for url in f:
            url = url.strip().replace("/blob/", "/raw/")
            print(f"\tretrieving {url}")
            download_file(url, P(url).name)


def concat_snippets(snippets: str) -> None:
    """
    Concatenates *.gitignore-snippets to create .gitignore.
    """
    script_dir = P(__file__).parent
    gil = set(glob(f"{script_dir}{os.sep}*.gitignore"))
    gil.discard(".gitignore")  # Remove .gitignore from the set if it exists
    s2u = get_snippet_to_url(snippets)
    with P(TARGET).open("w") as outfile:
        outfile.write(f"# .gitignore created by {P(__file__).name}\n")
        outfile.write(f"# see {GITHUB_PROJECT}\n")
        for gi in gil:
            gin = P(gi).name
            print(f"\tappending {gin}")
            outfile.write(f"# Contents of {gin}\n")
            outfile.write(f"# from {s2u.get(gin, '- no url -')}\n")
            for line in read_file(gi):
                outfile.write(line)
            outfile.write("\n\n")


def custom_help_check() -> None:
    """
    Adds command line options -h and -? in addition to the default --help to
    show help output.
    """
    if "-h" in sys.argv or "-?" in sys.argv:
        sys.argv[1] = "--help"


def main(
    snippets: str = typer.Argument(
        "gitignore-snippets.txt",
        help="gitignore-snippets file name",
    ),
    update_gitignores: bool = typer.Option(
        False,
        "--update-gitignores",
        "-u",
        help=("update gitignores " "listed in SNIPPETS"),
    ),
) -> None:
    """
    Concatenates gitignore-snippets found in the local directory to form a target
    .gitignore.

    Optionally refreshes snippets listed in gitignore-snippets.txt beforehand by
    downloading them.
    """
    if update_gitignores:
        get_snippets(snippets)
    print(f"generating {TARGET}")
    concat_snippets(snippets)
    print(f"done generating {TARGET}.")


if __name__ == "__main__":
    custom_help_check()
    typer.run(main)
