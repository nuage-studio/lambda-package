import unittest
from pathlib import Path

from lambda_package import find_paths


class LambdaPackageFindPathsTests(unittest.TestCase):
    """
    Unit tests for the `lambda_package.find_paths` function
    """

    def test_find_paths_list(self):
        (excludes, dirs) = get_test_data()
        (paths, tree) = find_paths(dirs, excludes)
        path_strings = [str(path) for path in paths]

        self.assertSetEqual(
            set(path_strings),
            {
                "something.png",
                "bar/nothello",
                "a/goo.txt",
                "a/b/goo.txt",
            },
        )

    def test_find_paths_tree(self):
        (excludes, dirs) = get_test_data()
        (paths, tree) = find_paths(dirs, excludes)
        files_list = tree_to_list(tree)

        self.assertSetEqual(
            set(files_list),
            {
                "something.png",
                "bar/nothello",
                "a/goo.txt",
                "a/b/goo.txt",
            },
        )


def tree_to_list(tree, path=""):
    files_list = []

    for d in tree[1]:
        files_list.extend(tree_to_list(d, str(Path(path).joinpath(d[0]))))

    for f in tree[2]:
        files_list.append(str(Path(path).joinpath(f.name)))

    return files_list


def get_test_data():

    excludes = [".*", "*.jpg", "foo/", "bar/hello*", "moo.txt"]

    dirs = MockPath(
        ".",
        [MockPath("moo.txt"), MockPath("something.png"), MockPath("something.jpg")],
        [
            MockPath("foo", [MockPath("foo/bar.txt"), MockPath("foo/baz.txt")]),
            MockPath(
                "bar",
                [
                    MockPath("bar/hello"),
                    MockPath("bar/hello.txt"),
                    MockPath("bar/nothello"),
                ],
            ),
            MockPath(
                "a",
                [MockPath("a/moo.txt"), MockPath("a/goo.txt")],
                [MockPath("b", [MockPath("a/b/moo.txt"), MockPath("a/b/goo.txt")])],
            ),
        ],
    )

    return (excludes, dirs)


class MockPath:
    def __init__(self, path, files=None, dirs=None):
        self.path = Path(path)
        self.name = self.path.name
        self.is_directory = files is not None or dirs is not None
        self.files = files if files else []
        self.dirs = dirs if dirs else []

    def iterdir(self):
        return [*self.dirs, *self.files]

    def is_dir(self):
        return self.is_directory

    def __str__(self):
        return str(self.path)
