from pathlib import Path
from platform import python_version as get_python_version
from typing import List, Optional

from toml import load

ConfigFileName = ".lambda-packagerc"
SetupFileName = "setup.cfg"
TomlSectionName = "lambda-package"

ValidKeys = [
    "output",
    "exclude",
    "requirements",
    "layer_output",
    "use_docker",
    "python_version",
]


class Configuration:
    """
    Represents the packager configuration.  Instances of this object can be
    passed to the `package` method.

    To create a Configuration object, either use the constructor directly, or call
    the `create_from_config_file` method.
    """

    output: Optional[str]
    """
    The file path of the zip file which is output by the packager.  Leave as
    `None` to generate no output.
    """

    exclude: List[str]
    """
    A list of file exclude patterns which should not be packaged.
    """

    requirements: Optional[str]
    """
    The path to the requirements.txt file if Python dependencies are to be packaged.
    """

    layer_output: Optional[str]
    """
    Path to a folder where requirement outputs should be stored.
    """

    use_docker: bool
    """
    Whether or not the Lambda layer should be compiled using a Docker image.
    """

    python_version: str
    """
    The Python version used by Docker to package the requirements.
    """

    def __init__(
        self,
        output: Optional[str] = None,
        exclude: List[str] = None,
        requirements: Optional[str] = None,
        layer_output: Optional[str] = None,
        use_docker: Optional[bool] = True,
        python_version: Optional[str] = get_python_version(),
    ):
        self.output = output
        self.exclude = exclude
        self.requirements = requirements
        self.layer_output = layer_output
        self.use_docker = use_docker
        self.python_version = python_version

    @staticmethod
    def create_from_config_file():
        """
        This methods creates a Configuration object by attempting to read parameters
        from two TOML files: `.lambda-packagerc` and `setup.cfg`.  The
        `.lambda-packagerc` takes precedence for any values which appear in both,
        and defaults are used for any values which are not present, or if the files do
        not exist.  In the TOML files parameters must be under a section called
        `[lambda-package]`, and the parameter key names are the same as the attributes
        of this class.
        """
        rc_config_dict = Configuration.read_config_dict(ConfigFileName)
        setup_config_dict = Configuration.read_config_dict(SetupFileName)
        config_dict = {**setup_config_dict, **rc_config_dict}

        for key in config_dict.keys():
            if key not in ValidKeys:
                raise KeyError(f"Parameter {key} is not valid")

        return Configuration(**config_dict)

    @staticmethod
    def read_config_dict(path: str):
        """
        Reads the [lambda-package] section from a TOML configuration file into a
        dictionary, or returns an empty dictionary if the file does not exist.

        :param path     The path to the TOML configuration file.
        """
        if Path(path).exists():
            config_dict = load(path)

            if TomlSectionName in config_dict.keys():
                return config_dict.get(TomlSectionName)

        return {}
