from datetime import datetime
from random import choice
from re import compile
from shutil import copy
from string import ascii_lowercase
from subprocess import run
from tempfile import gettempdir

from docker import from_env
from lambda_package.lambda_package import Configuration, Path

"""
The functions in this file help to build an Lambda's Python requirements into a
temporary directory, either using Docker or using pip on the local machine.
"""

TempDir = gettempdir()
VersionRegex = compile("(^[0-9]+\\.[0-9]+)(\\.[0-9]+)?$")


def build_requirements(configuration: Configuration) -> str:
    """
    Builds the `pip` requirements into a temporary directory, and returns a path
    to that directory.  If `use_docker` is `True`, the requirements are built using
    a Lambda Docker image.  Otherwise, pip will be called locally.
    """
    if configuration.use_docker:
        return build_requirements_docker(configuration)
    else:
        return build_requirements_local(configuration)


def build_requirements_docker(configuration: Configuration):

    temp_dir = create_temp_requirements_directory()

    # Copy the requirements file into the directory
    requirements_src_path = Path(configuration.requirements)
    requirements_dest_path = temp_dir.joinpath(requirements_src_path.name)
    copy(str(requirements_src_path), str(requirements_dest_path))

    # Launch the Docker instance to install the requirements
    client = from_env()
    vols = {str(temp_dir): {"bind": "/var/task", "mode": "z"}}
    python_version = normalize_version(configuration.python_version)
    client.containers.run(
        f"lambci/lambda:build-python{python_version}",
        f"pip install -t /var/task/ -r /var/task/{requirements_dest_path.name}",
        volumes=vols,
    )

    # Remove the copied requirements file
    requirements_dest_path.unlink()

    return temp_dir


def build_requirements_local(configuration: Configuration):
    temp_dir = create_temp_requirements_directory()
    print("temp dir ", temp_dir)
    run(["pip", "install", "-t", temp_dir, "-r", configuration.requirements])
    return temp_dir


def create_temp_requirements_directory():
    """
    Create a temporary directory in which to install requirements so they can be zipped
    """
    temp_dir = Path(TempDir).joinpath(generate_temp_directory_name()).absolute()
    temp_dir.mkdir(parents=True)
    return temp_dir


def generate_temp_directory_name():
    """
    Generate a temporary directory name
    """
    random_chars = "".join(choice(ascii_lowercase) for i in range(8))
    timestamp = datetime.now().strftime("%d%m%Y%H%M%S")
    return f"requirements_task_dir_{timestamp}_{random_chars}"


def normalize_version(version_string):
    """
    Normalize a Python version string to be in the form: `[major].[minor]`, as this
    is the format required by the Docker instance.  This means the patch number will be
    discarded if present, and any other format will raise a ValueError.

    """
    m = VersionRegex.match(version_string)

    if m is None:
        raise ValueError(
            f"Invalid Python version: '{version_string}'.  Version must be in the form [major].[minor]"
        )

    return m.group(1)
