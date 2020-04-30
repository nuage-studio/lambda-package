import unittest
from unittest import mock
from unittest.mock import Mock

from lambda_package.configuration import ConfigFileName, Configuration, SetupFileName


class PackageTests(unittest.TestCase):
    @mock.patch("lambda_package.Configuration.read_config_dict")
    def test_create_from_config_file(self, read_config_dict_mock: Mock):
        read_config_dict_mock.return_value = {
            "output": "my_output",
            "exclude": ["my_exclude1", "my_exclude2"],
        }

        configuration = Configuration.create_from_config_file()
        self.assertEqual(configuration.output, "my_output")
        self.assertEqual(configuration.exclude, ["my_exclude1", "my_exclude2"])

    @mock.patch("lambda_package.Configuration.read_config_dict")
    def test_when_rc_file_has_output_and_setup_file_doesnt_then_config_has_rc_value(
        self, read_config_dict_mock: Mock
    ):
        def read_config_dict(path):
            if path == ConfigFileName:
                return {"output": "myoutput_rc"}
            else:
                return {}

        read_config_dict_mock.side_effect = read_config_dict

        configuration = Configuration.create_from_config_file()
        self.assertEqual(configuration.output, "myoutput_rc")

    @mock.patch("lambda_package.Configuration.read_config_dict")
    def test_when_setup_file_has_output_and_rc_file_doesnt_then_config_has_setup_value(
        self, read_config_dict_mock: Mock
    ):
        def read_config_dict(path):
            if path == SetupFileName:
                return {"output": "myoutput_setup"}
            else:
                return {}

        read_config_dict_mock.side_effect = read_config_dict

        configuration = Configuration.create_from_config_file()
        self.assertEqual(configuration.output, "myoutput_setup")

    @mock.patch("lambda_package.Configuration.read_config_dict")
    def test_when_setup_file_has_output_and_rc_file_has_output_then_config_has_rc_value(
        self, read_config_dict_mock: Mock
    ):
        def read_config_dict(path):
            if path == ConfigFileName:
                return {"output": "myoutput_rc"}
            elif path == SetupFileName:
                return {"output": "myoutput_setup"}

        read_config_dict_mock.side_effect = read_config_dict

        configuration = Configuration.create_from_config_file()
        self.assertEqual(configuration.output, "myoutput_rc")

    @mock.patch("lambda_package.Configuration.read_config_dict")
    def test_when_config_file_contains_invalid_key_then_throw_exception(
        self, read_config_dict_mock: Mock
    ):
        read_config_dict_mock.return_value = {"blah": 123}

        with self.assertRaises(KeyError):
            Configuration.create_from_config_file()
