import unittest
from unittest import mock
from unittest.mock import Mock

from lambda_package.configuration import Configuration


class PackageTests(unittest.TestCase):
    @mock.patch("lambda_package.Configuration.read_config_dict")
    def test_create_from_config_file(self, read_config_dict_mock: Mock):
        read_config_dict_mock.return_value = {"output": "myoutput123"}
        configuration = Configuration.create_from_config_file()
        self.assertEqual(configuration.output, "myoutput123")
