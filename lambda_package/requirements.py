from datetime import datetime
from random import choice
from shutil import copy
from string import ascii_lowercase

from docker import from_env
from lambda_package.lambda_package import Configuration, Path

"""
The functions in this file help to build an Lambda's Python requirements into a
temporary directory, either using Docker or using pip on the local machine.
"""

CacheDir = ".lambda-package"


def build_requirements(configuration: Configuration):
    if configuration.use_docker:
        temp_dir = Path(CacheDir).joinpath(generate_temp_task_dir()).absolute()
        temp_dir.mkdir(parents=True)

        requirements_src_path = Path(configuration.requirements)
        requirements_dest_path = temp_dir.joinpath(requirements_src_path.name)

        copy(str(requirements_src_path), str(requirements_dest_path))

        vols = {str(temp_dir): {"bind": "/var/task", "mode": "z"}}

        client = from_env()
        client.containers.run(
            f"lambci/lambda:build-python{configuration.python_version}",
            f"pip install -t /var/task/ -r /var/task/{requirements_src_path.name}",
            volumes=vols,
        )

        return temp_dir

    else:
        raise Exception("Currently requirements can only built using docker")


def generate_temp_task_dir():
    """
    Generate a temporary directory name for the Lambda's `task` directory for Docker
    """
    random_chars = "".join(choice(ascii_lowercase) for i in range(8))
    timestamp = datetime.now().strftime("%d%m%Y%H%M%S")
    return f"requirements_task_dir_{timestamp}_{random_chars}"
