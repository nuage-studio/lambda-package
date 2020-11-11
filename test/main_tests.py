import unittest
from unittest import mock
from unittest.mock import Mock

from lambda_package import Configuration
from lambda_package.__main__ import get_configuration


@mock.patch("lambda_package.Configuration.create_from_config_file")
class LambdaPackageTests(unittest.TestCase):
    """
    General unit tests for the `__main__` module
    """

    def test_when_output_arg_given_then_overrides_configuration(
        self, create_from_config_file_mock: Mock
    ):

        create_from_config_file_mock.return_value = Configuration(
            output="my_output_config"
        )

        args = Mock()
        args.output = "my_output_arg"
        args.layer_only = False

        validated_config = get_configuration(args)

        self.assertEqual(validated_config.output, args.output)

    def test_when_layer_only_given_then_output_is_none(
        self, create_from_config_file_mock: Mock
    ):

        create_from_config_file_mock.return_value = Configuration(
            output="my_output", layer_output="my_layer_output"
        )

        args = Mock()
        args.output = None
        args.layer_only = True

        validated_config = get_configuration(args)

        self.assertEqual(validated_config.output, None)

    def test_when_layer_only_but_no_layer_output_then_error(
        self, create_from_config_file_mock: Mock
    ):

        create_from_config_file_mock.return_value = Configuration(
            output="my_output", layer_output=None,
        )

        args = Mock()
        args.output = None
        args.layer_only = True

        self.assertRaisesRegex(
            ValueError,
            "A layer output must be specified when using --layer-only",
            get_configuration,
            args,
        )

    def test_when_layer_only_and_output_given_then_raises_error(
        self, create_from_config_file_mock: Mock
    ):

        create_from_config_file_mock.return_value = Configuration(
            output="my_output", layer_output="my_layout_output",
        )

        args = Mock()
        args.output = "my_output"
        args.layer_only = True

        self.assertRaisesRegex(
            ValueError,
            "The --layer-only and --output parameters cannot be used together",
            get_configuration,
            args,
        )
