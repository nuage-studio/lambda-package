import unittest
from pathlib import Path
from unittest import mock
from unittest.mock import Mock

from lambda_package.configuration import Configuration
from lambda_package.requirements import CacheDir, build_requirements


class RequirementsTests(unittest.TestCase):
    @mock.patch("pathlib.Path.mkdir")
    @mock.patch("lambda_package.requirements.copy")
    @mock.patch("lambda_package.requirements.generate_temp_task_dir")
    @mock.patch("lambda_package.requirements.from_env")
    def test_when_requirements_given_and_use_docker_given_then_docker_is_called(
        self,
        from_env_mock: Mock,
        generate_temp_task_dir_mock: Mock,
        copy_mock: Mock,
        mkdir_mock,
    ):
        generate_temp_task_dir_mock.return_value = "my_temp_dir"
        run_mock = Mock()
        from_env_mock.return_value = Mock()
        from_env_mock.return_value.containers.run = run_mock
        expected_temp_dir = Path(CacheDir).joinpath("my_temp_dir").absolute()

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

    @mock.patch("pathlib.Path.mkdir")
    @mock.patch("lambda_package.requirements.copy")
    @mock.patch("lambda_package.requirements.generate_temp_task_dir")
    @mock.patch("lambda_package.requirements.from_env")
    def test_when_build_requirements_is_called_then_returns_requirements_directory(
        self,
        from_env_mock: Mock,
        generate_temp_task_dir_mock: Mock,
        copy_mock: Mock,
        mkdir_mock,
    ):
        generate_temp_task_dir_mock.return_value = "my_temp_dir"
        run_mock = Mock()
        from_env_mock.return_value = Mock()
        from_env_mock.return_value.containers.run = run_mock
        expected_temp_dir = Path(CacheDir).joinpath("my_temp_dir").absolute()

        res = build_requirements(
            Configuration(requirements="my_requirements", use_docker=True)
        )

        self.assertEqual(res, expected_temp_dir)
