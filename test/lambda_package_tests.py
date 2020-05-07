import unittest
from unittest import mock
from unittest.mock import ANY, Mock

from lambda_package import package
from lambda_package.configuration import Configuration


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
        find_paths_mock.return_value = ("mypaths", "")
        package(configuration=Configuration(output="myoutput"))
        zip_package_mock.assert_called_once_with(paths="mypaths", fp="myoutput")

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
        find_paths_mock.return_value = ("mypaths", "")
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
        find_paths_mock.return_value = ("mypaths", "")
        package(configuration=Configuration())
        create_from_config_file_mock.assert_not_called()

    @mock.patch("lambda_package.lambda_package.find_excludes")
    @mock.patch("lambda_package.lambda_package.find_paths")
    @mock.patch("lambda_package.lambda_package.zip_package")
    def test_when_config_has_no_excludes_then_read_gitignore(
        self, zip_package_mock: Mock, find_paths_mock: Mock, find_excludes_mock: Mock
    ):
        find_excludes_mock.return_value = ["gitignoreex"]
        find_paths_mock.return_value = ("mypaths", "")
        package(configuration=Configuration())

        find_excludes_mock.assert_called_once()
        find_paths_mock.assert_called_once_with(root_path=ANY, excludes=["gitignoreex"])

    @mock.patch("lambda_package.lambda_package.find_excludes")
    @mock.patch("lambda_package.lambda_package.find_paths")
    @mock.patch("lambda_package.lambda_package.zip_package")
    def test_when_config_has_excludes_then_do_not_read_gitignore(
        self, zip_package_mock: Mock, find_paths_mock: Mock, find_excludes_mock: Mock
    ):
        find_excludes_mock.return_value = []
        find_paths_mock.return_value = ("mypaths", "")
        package(configuration=Configuration(exclude=["myexclude"]))

        find_excludes_mock.assert_not_called()
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
        find_paths_mock.return_value = (["mypath"], "")
        get_files_in_directory_mock.return_value = ["myreqfile"]
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
        find_paths_mock.return_value = ("mypaths", "")
        package(configuration=Configuration())
        build_requirements_mock.assert_not_called()
