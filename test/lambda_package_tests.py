import unittest
from pathlib import Path
from unittest import mock
from unittest.mock import Mock

from lambda_package.lambda_package import get_files_in_directory, get_zip_package_paths


class LambdaPackageTests(unittest.TestCase):
    """
    General unit tests for the `lambda_package` module
    """

    @mock.patch("lambda_package.lambda_package.walk")
    def test_when_call_get_files_in_directory_then_calls_os_walk(self, walk_mock: Mock):
        walk_mock.return_value = [
            (".", ["dir1", "dir2"], ["req_file_1", "req_file_2"]),
            ("./dir1", [], ["req_file_3", "req_file_4"]),
            ("./dir2", [], ["req_file_5", "req_file_6"]),
        ]

        files = get_files_in_directory("my_temp_dir")

        walk_mock.assert_called_once_with("my_temp_dir")
        self.assertSetEqual(
            {str(file) for file in files},
            set(
                [
                    "req_file_1",
                    "req_file_2",
                    "dir1/req_file_3",
                    "dir1/req_file_4",
                    "dir2/req_file_5",
                    "dir2/req_file_6",
                ]
            ),
        )

    def test_when_call_get_zip_package_paths_then_paths_are_relative_to_root(self):

        result = get_zip_package_paths(
            paths=[
                Path("dir1/dir2/dir3/dir4/my_file1"),
                Path("dir1/dir2/dir3/dir5/my_file2"),
            ],
            root_dir=Path("dir1").joinpath("dir2"),
        )

        self.assertListEqual(
            [
                (Path("dir1/dir2/dir3/dir4/my_file1"), Path("dir3/dir4/my_file1")),
                (Path("dir1/dir2/dir3/dir5/my_file2"), Path("dir3/dir5/my_file2")),
            ],
            result,
        )
