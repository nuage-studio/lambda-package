from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="lambda-package",
    version="1.0.0",
    author="Nuage Studio",
    description="A library and command-line tool to package up Lambda functions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nuage-studio/lambda-package",
    packages=find_packages(),
    python_requires=">=3.7",
    install_requires=["pathspec>=0.8.0", "toml>=0.10.0", "docker>=4.2.0"],
    test_requires=[],
    test_suite="test",
)
