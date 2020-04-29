# Nuage Lambda Packaging

This repository provides both a library function and command-line tool to package up Lambda functions.
Given a directory, it will package all the files in the directory into a zip file, but ignoring any files
covered by the `.gitignore` file in the current directory.

## Command line useage

To use on the command line, you should install the package using pip, and then use the following command:

```
python -m lambda_package path [--output OUTPUT]
```

where `path` is the path to the source directory which you wish to package, and the
`--output` (or `-o`) option specifies the zip file output.  If no `-o` option is given,
the tool will display a preview of the file tree which it would package.


## Library usage

The package also exposes a function named `package`, which performs the same function
as the command line.  For example:

```python
from lambda_package import package

package(root_path="src", Configuration(output="app.zip"))
```


# Development

## Getting started

You need Python 3 (preferably 3.8) installed to start working on this project.

In order to install your virtualenv, just go to the root of the project and:
```bash
make install
```

## IDE

Nuage recommends [Visual Studio Code](https://code.visualstudio.com/download) to work on this project, and some default settings have been configured in the [.vscode/settings.json](.vscode/settings.json).

These settings merely enforce the code-quality guidelines defined below, but if you use another IDE it's probably worth taking a quick look at it to ensure compliance with the standard.

By default, we recommend:
1. Putting your virtualenv in a `venv` folder at the project root
2. Using a `.env` file to define your environment variables (cf. [python-dotenv](https://pypi.org/project/python-dotenv/))

## Code quality

This project has opinionated code-quality requirements:
- Code formatter: [black](https://black.readthedocs.io/en/stable/)
- Code linter: [pylint](https://www.pylint.org)
- Code style guidelines: [flake8](https://flake8.pycqa.org/en/latest/)

All of these tools are enforced at the commit-level via [pre-commit](https://pre-commit.com)

You can run the following command to apply code-quality to your project at any point:
```bash
make quality
```

Code quality configuration files:
- IDE-agnostic coding style settings are set in the [.editorconfig](.editorconfig) file
- Python-related settings are set in the [setup.cfg](setup.cfg) file
- Pre-commit-related settings are set in the [.pre-commit-config.yaml](.pre-commit-config.yaml) file
