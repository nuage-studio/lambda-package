import unittest
from pathlib import Path
from unittest import mock
from unittest.mock import ANY, Mock

from lambda_package import package
from lambda_package.configuration import Configuration


@mock.patch("lambda_package.lambda_package.rmtree")
@mock.patch("lambda_package.lambda_package.find_paths")
@mock.patch("lambda_package.lambda_package.zip_package")
@mock.patch("lambda_package.Configuration.create_from_config_file")
@mock.patch("lambda_package.lambda_package.read_gitignore")
@mock.patch("lambda_package.lambda_package.build_requirements")
@mock.patch("lambda_package.lambda_package.get_files_in_directory")
class LambdaPackagePackageTests(unittest.TestCase):
    """
    Unit tests for the `lambda_package.package` function
    """

    def test_when_no_output_specified_then_zip_package_not_called(
        self,
        get_files_in_directory_mock: Mock,
        build_requirements_mock: Mock,
        read_gitignore_mock: Mock,
        create_from_config_file_mock: Mock,
        zip_package_mock: Mock,
        find_paths_mock: Mock,
        rmtree_mock: Mock,
    ):
        find_paths_mock.return_value = ("", "")
        package(configuration=Configuration())
        zip_package_mock.assert_not_called()

    def test_when_output_specified_then_zip_package_called(
        self,
        get_files_in_directory_mock: Mock,
        build_requirements_mock: Mock,
        read_gitignore_mock: Mock,
        create_from_config_file_mock: Mock,
        zip_package_mock: Mock,
        find_paths_mock: Mock,
        rmtree_mock: Mock,
    ):
        find_paths_mock.return_value = ([Path("mypaths")], "")
        package(configuration=Configuration(output="myoutput"))
        zip_package_mock.assert_called_once_with(
            paths=[(Path("mypaths"), Path("mypaths"))], fp="myoutput"
        )

    def test_when_root_path_given_then_zip_package_called_with_relative_paths(
        self,
        get_files_in_directory_mock: Mock,
        build_requirements_mock: Mock,
        read_gitignore_mock: Mock,
        create_from_config_file_mock: Mock,
        zip_package_mock: Mock,
        find_paths_mock: Mock,
        rmtree_mock: Mock,
    ):
        find_paths_mock.return_value = ([Path("src/mypaths")], "")
        package(configuration=Configuration(output="myoutput"), root_path="src")
        zip_package_mock.assert_called_once_with(
            paths=[(Path("src/mypaths"), Path("mypaths"))], fp="myoutput"
        )

    def test_when_config_not_given_then_read_from_disk(
        self,
        get_files_in_directory_mock: Mock,
        build_requirements_mock: Mock,
        read_gitignore_mock: Mock,
        create_from_config_file_mock: Mock,
        zip_package_mock: Mock,
        find_paths_mock: Mock,
        rmtree_mock: Mock,
    ):
        create_from_config_file_mock.return_value = Configuration()
        find_paths_mock.return_value = ([Path("mypaths")], "")
        package()
        create_from_config_file_mock.assert_called_once()

    def test_when_config_given_then_do_not_read_from_disk(
        self,
        get_files_in_directory_mock: Mock,
        build_requirements_mock: Mock,
        read_gitignore_mock: Mock,
        create_from_config_file_mock: Mock,
        zip_package_mock: Mock,
        find_paths_mock: Mock,
        rmtree_mock: Mock,
    ):
        create_from_config_file_mock.return_value = Configuration()
        find_paths_mock.return_value = ([Path("mypaths")], "")
        package(configuration=Configuration())
        create_from_config_file_mock.assert_not_called()

    def test_when_config_has_no_excludes_then_read_gitignore(
        self,
        get_files_in_directory_mock: Mock,
        build_requirements_mock: Mock,
        read_gitignore_mock: Mock,
        create_from_config_file_mock: Mock,
        zip_package_mock: Mock,
        find_paths_mock: Mock,
        rmtree_mock: Mock,
    ):
        read_gitignore_mock.return_value = ["gitignoreex"]
        find_paths_mock.return_value = ([Path("mypaths")], "")
        package(configuration=Configuration())

        read_gitignore_mock.assert_called_once()
        find_paths_mock.assert_called_once_with(root_path=ANY, excludes=["gitignoreex"])

    def test_when_config_has_excludes_then_do_not_read_gitignore(
        self,
        get_files_in_directory_mock: Mock,
        build_requirements_mock: Mock,
        read_gitignore_mock: Mock,
        create_from_config_file_mock: Mock,
        zip_package_mock: Mock,
        find_paths_mock: Mock,
        rmtree_mock: Mock,
    ):
        read_gitignore_mock.return_value = []
        find_paths_mock.return_value = ([Path("mypaths")], "")
        package(configuration=Configuration(exclude=["myexclude"]))

        read_gitignore_mock.assert_not_called()
        find_paths_mock.assert_called_once_with(root_path=ANY, excludes=["myexclude"])

    def test_when_requirements_given_then_call_build_requirements(
        self,
        get_files_in_directory_mock: Mock,
        build_requirements_mock: Mock,
        read_gitignore_mock: Mock,
        create_from_config_file_mock: Mock,
        zip_package_mock: Mock,
        find_paths_mock: Mock,
        rmtree_mock: Mock,
    ):
        read_gitignore_mock.return_value = []
        find_paths_mock.return_value = ([Path("mypath")], "")
        build_requirements_mock.return_value = Path("my_temp_dir")
        get_files_in_directory_mock.return_value = [Path("my_temp_dir/myreqfile")]
        package(configuration=Configuration(requirements="my_requirements"))
        build_requirements_mock.assert_called_once()

    def test_when_requirements_not_given_then_do_not_call_build_requirements(
        self,
        get_files_in_directory_mock: Mock,
        build_requirements_mock: Mock,
        read_gitignore_mock: Mock,
        create_from_config_file_mock: Mock,
        zip_package_mock: Mock,
        find_paths_mock: Mock,
        rmtree_mock: Mock,
    ):
        read_gitignore_mock.return_value = []
        find_paths_mock.return_value = ([Path("mypaths")], "")
        package(configuration=Configuration())
        build_requirements_mock.assert_not_called()

    def test_when_requirements_given_and_no_layer_output_given_then_add_files_to_main_zip(
        self,
        get_files_in_directory_mock: Mock,
        build_requirements_mock: Mock,
        read_gitignore_mock: Mock,
        create_from_config_file_mock: Mock,
        zip_package_mock: Mock,
        find_paths_mock: Mock,
        rmtree_mock: Mock,
    ):
        read_gitignore_mock.return_value = []
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

    def test_when_requirements_given_and_layer_output_given_then_seperate_zip_created(
        self,
        get_files_in_directory_mock: Mock,
        build_requirements_mock: Mock,
        read_gitignore_mock: Mock,
        create_from_config_file_mock: Mock,
        zip_package_mock: Mock,
        find_paths_mock: Mock,
        rmtree_mock: Mock,
    ):
        read_gitignore_mock.return_value = []
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
