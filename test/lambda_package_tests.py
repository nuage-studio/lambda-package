import unittest
from unittest import mock
from unittest.mock import Mock

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
