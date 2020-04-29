from typing import List, Optional

ConfigFileName = ".lambda-packagerc"
SetupFileName = "setup.cfg"


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
