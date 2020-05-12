import unittest
from pathlib import Path
from unittest import mock
from unittest.mock import Mock

from lambda_package.configuration import Configuration
from lambda_package.requirements import TempDir, build_requirements


@mock.patch("lambda_package.requirements.run")
@mock.patch("pathlib.Path.mkdir")
@mock.patch("pathlib.Path.unlink")
@mock.patch("lambda_package.requirements.copy")
@mock.patch("lambda_package.requirements.generate_temp_directory_name")
@mock.patch("lambda_package.requirements.from_env")
class RequirementsTests(unittest.TestCase):
    """
    General unit tests for the `requirements` module
    """

    def test_when_requirements_given_and_use_docker_true_then_docker_is_called(
        self,
        from_env_mock: Mock,
        generate_temp_task_dir_mock: Mock,
        copy_mock: Mock,
        unlink_mock,
        mkdir_mock,
        subprocess_run_mock,
    ):
        generate_temp_task_dir_mock.return_value = "my_temp_dir"
        run_mock = Mock()
        from_env_mock.return_value = Mock()
        from_env_mock.return_value.containers.run = run_mock
        expected_temp_dir = Path(TempDir).joinpath("my_temp_dir").absolute()

        build_requirements(
            Configuration(
                requirements="my_requirements", use_docker=True, python_version="5.6"
            )
        )

        run_mock.assert_called_once_with(
            "lambci/lambda:build-python5.6",
            f"pip install -t /var/task/ -r /var/task/my_requirements",
            volumes={str(expected_temp_dir): {"bind": "/var/task", "mode": "z"}},
        )

    def test_when_build_requirements_is_called_then_returns_requirements_directory(
        self,
        from_env_mock: Mock,
        generate_temp_task_dir_mock: Mock,
        copy_mock: Mock,
        unlink_mock,
        mkdir_mock,
        subprocess_run_mock,
    ):
        generate_temp_task_dir_mock.return_value = "my_temp_dir"
        run_mock = Mock()
        from_env_mock.return_value = Mock()
        from_env_mock.return_value.containers.run = run_mock
        expected_temp_dir = Path(TempDir).joinpath("my_temp_dir").absolute()

        res = build_requirements(
            Configuration(requirements="my_requirements", use_docker=True)
        )

        self.assertEqual(res, expected_temp_dir)

    def test_when_requirements_given_and_use_docker_false_then_local_pip_is_called(
        self,
        from_env_mock: Mock,
        generate_temp_task_dir_mock: Mock,
        copy_mock: Mock,
        unlink_mock,
        mkdir_mock,
        subprocess_run_mock,
    ):
        generate_temp_task_dir_mock.return_value = "my_temp_dir"
        expected_temp_dir = Path(TempDir).joinpath("my_temp_dir").absolute()

        build_requirements(
            Configuration(
                requirements="my_requirements", use_docker=False, python_version="5.6"
            )
        )

        subprocess_run_mock.assert_called_once_with(
            ["pip", "install", "-t", expected_temp_dir, "-r", "my_requirements"]
        )
