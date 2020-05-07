import unittest
from pathlib import Path
from unittest import mock
from unittest.mock import Mock

from lambda_package import package
from lambda_package.configuration import Configuration
from lambda_package.lambda_package import get_files_in_directory
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
            set(files),
            set(
                [
                    "req_file_1",
                    "req_file_2",
                    "req_file_3",
                    "req_file_4",
                    "req_file_5",
                    "req_file_6",
                ]
            ),
        )

    @mock.patch("lambda_package.lambda_package.build_requirements")
    @mock.patch("lambda_package.lambda_package.get_files_in_directory")
    @mock.patch("lambda_package.lambda_package.find_excludes")
    @mock.patch("lambda_package.lambda_package.find_paths")
    @mock.patch("lambda_package.lambda_package.zip_package")
    def test_when_requirements_given_and_no_layer_then_add_files_to_zip(
        self,
        zip_package_mock: Mock,
        find_paths_mock: Mock,
        find_excludes_mock: Mock,
        get_files_in_directory_mock: Mock,
        build_requirements_mock: Mock,
    ):
        find_excludes_mock.return_value = []
        find_paths_mock.return_value = (["mypath1"], "")
        build_requirements_mock.return_value = "my_temp_dir"

        get_files_in_directory_mock.return_value = [
            "req_file_1",
            "req_file_2",
            "req_file_3",
            "req_file_4",
            "req_file_5",
            "req_file_6",
        ]

        package(
            configuration=Configuration(
                requirements="my_requirements", layer_output=None, output="my_output"
            )
        )

        get_files_in_directory_mock.assert_called_once_with("my_temp_dir")

        zip_package_mock.assert_called_once_with(
            paths=[
                "mypath1",
                "req_file_1",
                "req_file_2",
                "req_file_3",
                "req_file_4",
                "req_file_5",
                "req_file_6",
            ],
            fp="my_output",
        )
