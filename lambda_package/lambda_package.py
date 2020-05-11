import zipfile
from os import walk
from pathlib import Path
from typing import List, Tuple

import pathspec
from lambda_package.configuration import Configuration
from lambda_package.requirements import build_requirements


def package(root_path=".", configuration: Configuration = None):
    """
    Creates a zip package of the given directory, while excluding any files which
    have been specified in the exclude patterns.

    If no configuration value is provided, the function will attempt to read config
    values from disk.  See `Configuration.create_from_config_file` for more details.

    If no exclude patterns are given in the configuration, then the function will
    attempt to read patterns from the `.gitignore` file.

    If no output file is specified in the configuration then the zip package will not be
    generated, but the included files will still be returned.

    :param root_path        The path of the directory to package up
    :param configuration    The packager configuration.  See the `Configuration` class.
    :return A tuple with two elements:
        files_list  A list of pathlib files which did not meet the exclusion criteria
        files_tree  A recursive tuple in the form `(name, dirs, files)`,
                    similar to the output of `os.walk`, containing files which did not
                    meet the exclusion criteria
    """

    if not configuration:
        configuration = Configuration.create_from_config_file()

    if not configuration.exclude:
        configuration.exclude = find_excludes()

    (paths, tree) = find_paths(
        root_path=Path(root_path), excludes=configuration.exclude
    )
    zip_paths = get_zip_package_paths(paths=paths, root_dir=root_path)

    if configuration.requirements:
        requirements_dir = build_requirements(configuration)
        requirements_files = get_files_in_directory(requirements_dir)
        requirements_zip_paths = get_zip_package_paths(
            paths=requirements_files, root_dir=requirements_dir
        )

        if configuration.layer_output:
            zip_package(
                paths=requirements_zip_paths, fp=configuration.layer_output,
            )
        else:
            zip_paths.extend(requirements_zip_paths)

        # delete temp dir

    if configuration.output:
        zip_package(paths=zip_paths, fp=configuration.output)

    return (paths, tree)


def find_excludes():
    """
    Reads a list of exclude patterns from the `.gitignore` file in the local directory.
    A pattern for excluding hidden files is also added.
    """
    excludes = []
    gitignore = Path(".gitignore")
    if gitignore.exists():
        with gitignore.open() as f:
            excludes += f.read().split("\n")
    else:
        raise ValueError(
            "No exclude configuration option and no .gitignore file present"
        )
    return excludes


def find_paths(root_path, excludes):
    """
    Files all files in the `root_path` directory, excluding those which are covered by
    the exlusion patterns.

    :param root_path     The directory to be searched, as a `pathlib` path
    :param excludes      A list of .gitignore exclude patterns, or a pathspec
    :return A tuple with two elements:
        files_list  A list of pathlib files which did not meet the exclusion criteria
        files_tree  A recursive tuple in the form `(name, dirs, files)`,
                    similar to the output of `os.walk`, containing files which did not
                    meet the exclusion criteria
    """
    files_list = []
    files_tree = (root_path.name, [], [])

    exclude_spec = (
        excludes
        if isinstance(excludes, pathspec.PathSpec)
        else pathspec.PathSpec.from_lines("gitwildmatch", excludes)
    )

    for subpath in root_path.iterdir():
        if not exclude_spec.match_file(subpath):
            if subpath.is_dir():
                (sub_files_list, sub_files_tree) = find_paths(subpath, exclude_spec)
                files_tree[1].append(sub_files_tree)
                files_list.extend(sub_files_list)
            else:
                files_tree[2].append(subpath)
                files_list.append(subpath)

    return (files_list, files_tree)


def get_files_in_directory(dir_name: str):
    """
    Returns a list of all the files in the given directory.  Recursively searches
    subdirectories.
    """
    filenames = []

    for entry in walk(dir_name):
        root_dir = entry[0]
        dir_files = entry[2]
        filenames.extend([Path(root_dir).joinpath(file) for file in dir_files])

    return filenames


def get_zip_package_paths(paths: List[Path], root_dir=None) -> List[Tuple[Path, Path]]:
    """
    Given a list of Path objects, returns a list of tuples with the original path and
    the destination path within the package zip file.  The destination paths are
    simply the source paths but relative to `root_dir`.
    """
    return [(path, path.relative_to(root_dir)) for path in paths]


def zip_package(paths: List[Path], fp, compression=zipfile.ZIP_DEFLATED):
    """
    Takes a list of Path objects and compress those files into a zip archive
    """

    with zipfile.ZipFile(
        file=fp, mode="w", compression=compression, compresslevel=9
    ) as z:
        for path in paths:
            (local_path, zip_path) = path
            z.write(filename=str(path[0]), arcname=str(path[1]))
