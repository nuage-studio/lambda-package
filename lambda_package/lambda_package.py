import zipfile
from pathlib import Path

import pathspec
from lambda_package.configuration import Configuration


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

    if configuration.output:
        zip_package(paths=paths, fp=configuration.output)

    return (paths, tree)


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


def zip_package(paths, fp, compression=zipfile.ZIP_DEFLATED):
    """
    Takes a list of filepaths and compress those files into a zip archive
    """
    with zipfile.ZipFile(
        file=fp, mode="w", compression=compression, compresslevel=9
    ) as z:
        for p in paths:
            z.write(p)
