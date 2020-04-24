import argparse
from pathlib import Path

from .lambda_packaging import find_excludes, find_paths, zip_package


def main():
    """
    Main entry point of the Command
    """
    parser = argparse.ArgumentParser()
    add_arguments(parser)
    args = parser.parse_args()

    # Find filepaths that should be added to the package
    excludes = find_excludes()
    paths = find_paths(root_path=Path(args.path), excludes=excludes)
    if args.output:
        zip_package(paths=paths, fp=args.output)
    else:
        tree(paths)


def add_arguments(parser):
    parser.add_argument(
        "path", default=".", help="The path of the package source files",
    )
    parser.add_argument(
        "-o",
        "--output",
        required=False,
        help="Specifies file to which the output is written.",
    )


def tree(paths):
    """
    Displays a tree of the files about to be zipped
    """
    print("List of the files that would be included in the package:\n")
    for p in paths:
        depth = len(p.parts)
        spacer = "    " * (depth - 1)
        print(f"{spacer} {p.name}")
    print("\n", "To create the actual zip, you need to specify the --output parameter")


if __name__ == "__main__":
    main()
