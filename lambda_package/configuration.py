from pathlib import Path
from typing import List, Optional

from toml import load

ConfigFileName = ".lambda-packagerc"
SetupFileName = "setup.cfg"
TomlSectionName = "lambda-package"


class Configuration:
    """
    Represents the packager configuration.  Instances of this object can be
    passed to the `package` method.
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

    def __init__(self, output: Optional[str] = None, exclude: List[str] = []):
        self.output = output
        self.exclude = exclude

    @staticmethod
    def create_from_config_file():
        """
        This method creates a Configuration object by attempting to read parameters
        from the `.lambda-packagerc` file.  Default values are used for any values
        not present, or if the file does not exist.
        """
        config_dict = Configuration.read_config_dict()
        return Configuration(output=config_dict.get("output"))

    @staticmethod
    def read_config_dict():
        """
        Reads lambda-package TOML configuration into a dictionary, or returns
        an empty dictionary if the file does not exist.
        """
        if Path(ConfigFileName).exists():
            config_dict = load(ConfigFileName)

            if TomlSectionName in config_dict.keys():
                return config_dict.get(TomlSectionName)

        return {}
