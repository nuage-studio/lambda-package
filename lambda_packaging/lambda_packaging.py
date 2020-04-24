import zipfile
from pathlib import Path

import pathspec


def package(output_file: str, root_path="."):
    """
    Creates a zip package of the given directory, while excluding any files which
    are excluded by the `.gitignore`.

    :param output_file      The output zip file path
    :param root_path        The path of the directory to package up
    """
    excludes = find_excludes()

    paths = find_paths(root_path=Path(root_path), excludes=excludes)
    zip_package(paths=paths, fp=output_file)


def find_excludes():
    """
    Reads a list of exclude patterns from the `.gitignore` file in the local directory.
    A pattern for excluding hidden files is also added.
    """
    excludes = [
        ".*",  # Hidden files
    ]
    # Read .gitignore
    gitignore = Path(".gitignore")
    if gitignore.exists():
        with gitignore.open() as f:
            excludes += f.read().split("\n")
    else:
        raise ValueError("No .gitignore found")
    return excludes


def find_paths(root_path, excludes):
    """
    Files all files in the `root_path` directory, excluding those which are covered by
    the exlusion patterns.

    :param root_path     The directory to be searched, as a `pathlib` path
    :param excludes      A list of .gitignore exclude patterns, or a pathspec
    """
    files = []

    exclude_spec = (
        excludes
        if isinstance(excludes, pathspec.PathSpec)
        else pathspec.PathSpec.from_lines("gitwildmatch", excludes)
    )

    for subpath in root_path.iterdir():
        if not exclude_spec.match_file(subpath):
            if subpath.is_dir():
                files.extend(find_paths(subpath, exclude_spec))
            else:
                files.append(subpath)

    return files


def zip_package(paths, fp, compression=zipfile.ZIP_DEFLATED):
    """
    Takes a list of filepaths and compress those files into a zip archive
    """
    with zipfile.ZipFile(
        file=fp, mode="w", compression=compression, compresslevel=9
    ) as z:
        for p in paths:
            z.write(p)
