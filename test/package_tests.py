import unittest

from lambda_packaging import find_paths


class PackageTests(unittest.TestCase):
    def test_find_paths(self):

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

        paths = find_paths(dirs, excludes)
        path_strings = [str(path) for path in paths]

        self.assertSetEqual(
            set(path_strings),
            {"something.png", "bar/nothello", "a/goo.txt", "a/b/goo.txt",},
        )
        pass


class MockPath:
    def __init__(self, path, files=None, dirs=None):
        self.path = path
        self.is_directory = files is not None or dirs is not None
        self.files = files if files else []
        self.dirs = dirs if dirs else []

    def iterdir(self):
        return [*self.dirs, *self.files]

    def is_dir(self):
        return self.is_directory

    def __str__(self):
        return self.path
