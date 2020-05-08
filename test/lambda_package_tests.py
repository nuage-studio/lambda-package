import unittest
from pathlib import Path
from unittest import mock
from unittest.mock import ANY, Mock

from lambda_package import package
from lambda_package.configuration import Configuration
from lambda_package.lambda_package import get_files_in_directory, get_zip_package_paths


class PackageTests(unittest.TestCase):
    @mock.patch("lambda_package.lambda_package.find_paths")
    @mock.patch("lambda_package.lambda_package.zip_package")
    def test_when_no_output_specified_then_zip_package_not_called(
        self, zip_package_mock: Mock, find_paths_mock: Mock
    ):
        find_paths_mock.return_value = ("", "")
        package(configuration=Configuration())
        zip_package_mock.assert_not_called()

    @mock.patch("lambda_package.lambda_package.find_paths")
    @mock.patch("lambda_package.lambda_package.zip_package")
    def test_when_output_specified_then_zip_package_called(
        self, zip_package_mock: Mock, find_paths_mock: Mock
    ):
        find_paths_mock.return_value = ([Path("mypaths")], "")
        package(configuration=Configuration(output="myoutput"))
        zip_package_mock.assert_called_once_with(
            paths=[(Path("mypaths"), Path("mypaths"))], fp="myoutput"
        )

    @mock.patch("lambda_package.lambda_package.find_paths")
    @mock.patch("lambda_package.lambda_package.zip_package")
    def test_when_root_path_given_then_zip_package_called_with_relative_paths(
        self, zip_package_mock: Mock, find_paths_mock: Mock
    ):
        find_paths_mock.return_value = ([Path("src/mypaths")], "")
        package(configuration=Configuration(output="myoutput"), root_path="src")
        zip_package_mock.assert_called_once_with(
            paths=[(Path("src/mypaths"), Path("mypaths"))], fp="myoutput"
        )

    @mock.patch("lambda_package.Configuration.create_from_config_file")
    @mock.patch("lambda_package.lambda_package.find_paths")
    @mock.patch("lambda_package.lambda_package.zip_package")
    def test_when_config_not_given_then_read_from_disk(
        self,
        zip_package_mock: Mock,
        find_paths_mock: Mock,
        create_from_config_file_mock: Mock,
    ):
        create_from_config_file_mock.return_value = Configuration()
        find_paths_mock.return_value = ([Path("mypaths")], "")
        package()
        create_from_config_file_mock.assert_called_once()

    @mock.patch("lambda_package.Configuration.create_from_config_file")
    @mock.patch("lambda_package.lambda_package.find_paths")
    @mock.patch("lambda_package.lambda_package.zip_package")
    def test_when_config_given_then_do_not_read_from_disk(
        self,
        zip_package_mock: Mock,
        find_paths_mock: Mock,
        create_from_config_file_mock: Mock,
    ):
        create_from_config_file_mock.return_value = Configuration()
        find_paths_mock.return_value = ([Path("mypaths")], "")
        package(configuration=Configuration())
        create_from_config_file_mock.assert_not_called()

    @mock.patch("lambda_package.lambda_package.read_gitignore")
    @mock.patch("lambda_package.lambda_package.find_paths")
    @mock.patch("lambda_package.lambda_package.zip_package")
    def test_when_config_has_no_excludes_then_read_gitignore(
        self, zip_package_mock: Mock, find_paths_mock: Mock, read_gitignore_mock: Mock
    ):
        read_gitignore_mock.return_value = ["gitignoreex"]
        find_paths_mock.return_value = ([Path("mypaths")], "")
        package(configuration=Configuration())

        read_gitignore_mock.assert_called_once()
        find_paths_mock.assert_called_once_with(root_path=ANY, excludes=["gitignoreex"])

    @mock.patch("lambda_package.lambda_package.read_gitignore")
    @mock.patch("lambda_package.lambda_package.find_paths")
    @mock.patch("lambda_package.lambda_package.zip_package")
    def test_when_config_has_excludes_then_do_not_read_gitignore(
        self, zip_package_mock: Mock, find_paths_mock: Mock, read_gitignore_mock: Mock
    ):
        read_gitignore_mock.return_value = []
        find_paths_mock.return_value = ([Path("mypaths")], "")
        package(configuration=Configuration(exclude=["myexclude"]))

        read_gitignore_mock.assert_not_called()
        find_paths_mock.assert_called_once_with(root_path=ANY, excludes=["myexclude"])

    @mock.patch("lambda_package.lambda_package.build_requirements")
    @mock.patch("lambda_package.lambda_package.get_files_in_directory")
    @mock.patch("lambda_package.lambda_package.find_excludes")
    @mock.patch("lambda_package.lambda_package.find_paths")
    @mock.patch("lambda_package.lambda_package.zip_package")
    def test_when_requirements_given_then_call_build_requirements(
        self,
        zip_package_mock: Mock,
        find_paths_mock: Mock,
        find_excludes_mock: Mock,
        get_files_in_directory_mock: Mock,
        build_requirements_mock: Mock,
    ):
        find_excludes_mock.return_value = []
        find_paths_mock.return_value = ([Path("mypath")], "")
        build_requirements_mock.return_value = Path("my_temp_dir")
        get_files_in_directory_mock.return_value = [Path("my_temp_dir/myreqfile")]
        package(configuration=Configuration(requirements="my_requirements"))
        build_requirements_mock.assert_called_once()

    @mock.patch("lambda_package.lambda_package.build_requirements")
    @mock.patch("lambda_package.lambda_package.get_files_in_directory")
    @mock.patch("lambda_package.lambda_package.find_excludes")
    @mock.patch("lambda_package.lambda_package.find_paths")
    @mock.patch("lambda_package.lambda_package.zip_package")
    def test_when_requirements_not_given_then_do_not_call_build_requirements(
        self,
        zip_package_mock: Mock,
        find_paths_mock: Mock,
        find_excludes_mock: Mock,
        get_files_in_directory_mock: Mock,
        build_requirements_mock: Mock,
    ):
        find_excludes_mock.return_value = []
        find_paths_mock.return_value = ([Path("mypaths")], "")
        package(configuration=Configuration())
        build_requirements_mock.assert_not_called()

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

    @mock.patch("lambda_package.lambda_package.build_requirements")
    @mock.patch("lambda_package.lambda_package.get_files_in_directory")
    @mock.patch("lambda_package.lambda_package.find_excludes")
    @mock.patch("lambda_package.lambda_package.find_paths")
    @mock.patch("lambda_package.lambda_package.zip_package")
    def test_when_requirements_given_and_no_layer_output_given_then_add_files_to_main_zip(
        self,
        zip_package_mock: Mock,
        find_paths_mock: Mock,
        find_excludes_mock: Mock,
        get_files_in_directory_mock: Mock,
        build_requirements_mock: Mock,
    ):
        find_excludes_mock.return_value = []
        find_paths_mock.return_value = ([Path("mypath1")], "")
        build_requirements_mock.return_value = Path("my_temp_dir")

        get_files_in_directory_mock.return_value = [
            Path("my_temp_dir/req_file_1"),
            Path("my_temp_dir/req_file_2"),
            Path("my_temp_dir/req_file_3"),
            Path("my_temp_dir/req_file_4"),
            Path("my_temp_dir/req_file_5"),
            Path("my_temp_dir/req_file_6"),
        ]

        package(
            configuration=Configuration(
                requirements="my_requirements", layer_output=None, output="my_output"
            )
        )

        get_files_in_directory_mock.assert_called_once_with(Path("my_temp_dir"))

        zip_package_mock.assert_called_once_with(
            paths=[
                (Path("mypath1"), Path("mypath1")),
                (Path("my_temp_dir/req_file_1"), Path("req_file_1")),
                (Path("my_temp_dir/req_file_2"), Path("req_file_2")),
                (Path("my_temp_dir/req_file_3"), Path("req_file_3")),
                (Path("my_temp_dir/req_file_4"), Path("req_file_4")),
                (Path("my_temp_dir/req_file_5"), Path("req_file_5")),
                (Path("my_temp_dir/req_file_6"), Path("req_file_6")),
            ],
            fp="my_output",
        )

    @mock.patch("lambda_package.lambda_package.build_requirements")
    @mock.patch("lambda_package.lambda_package.get_files_in_directory")
    @mock.patch("lambda_package.lambda_package.find_excludes")
    @mock.patch("lambda_package.lambda_package.find_paths")
    @mock.patch("lambda_package.lambda_package.zip_package")
    def test_when_requirements_given_and_layer_output_given_then_seperate_zip_created(
        self,
        zip_package_mock: Mock,
        find_paths_mock: Mock,
        find_excludes_mock: Mock,
        get_files_in_directory_mock: Mock,
        build_requirements_mock: Mock,
    ):
        find_excludes_mock.return_value = []
        find_paths_mock.return_value = ([Path("mypath1")], "")
        build_requirements_mock.return_value = Path("my_temp_dir")

        get_files_in_directory_mock.return_value = [
            Path("my_temp_dir/req_file_1"),
            Path("my_temp_dir/req_file_2"),
            Path("my_temp_dir/req_file_3"),
        ]

        package(
            configuration=Configuration(
                requirements="my_requirements",
                layer_output="layer_out",
                output="my_output",
            )
        )

        get_files_in_directory_mock.assert_called_once_with(Path("my_temp_dir"))

        zip_package_mock.assert_any_call(
            paths=[
                (Path("my_temp_dir/req_file_1"), Path("req_file_1")),
                (Path("my_temp_dir/req_file_2"), Path("req_file_2")),
                (Path("my_temp_dir/req_file_3"), Path("req_file_3")),
            ],
            fp="layer_out",
        )

        zip_package_mock.assert_any_call(
            paths=[(Path("mypath1"), Path("mypath1"))], fp="my_output",
        )
