import argparse

from lambda_package.configuration import Configuration

from .lambda_package import package


def main():
    """
    Main entry point of the Command
    """
    parser = argparse.ArgumentParser("lambda_package")
    add_arguments(parser)
    args = parser.parse_args()
    configuration = Configuration.create_from_config_file()
    configuration.output = args.output if args.output else configuration.output

    (_, tree) = package(root_path=args.path, configuration=configuration)

    if not configuration.output and not configuration.layer_output:
        print_tree(tree)
    else:
        if configuration.output:
            print(f"Successfully created package {configuration.output}")
        if configuration.requirements and configuration.layer_output:
            print(f"Successfully created layer package {configuration.layer_output}")


def add_arguments(parser):
    parser.add_argument(
        "path", default=".", help="The path of the package source files.",
    )
    parser.add_argument(
        "-o",
        "--output",
        required=False,
        help="Specifies file to which the output is written.",
    )


def print_tree(files_tree):
    """
    Displays a tree of the files about to be zipped.

    :param files_tree   A recursive tuple in the form `(name, dirs, files)`,
                        similar to the output of `os.walk`.
    """
    print("List of the files that would be included in the package:\n")

    def print_tree_recurse(files_tree, depth):
        spacer = "│  " * (depth)

        # Recursively print all subdirectories
        for d in files_tree[1]:
            if len(d[1]) > 0 or len(d[2]) > 0:
                print(f"{spacer}└─ {d[0]}")
                print_tree_recurse(d, depth + 1)

        # Print all files in current directory
        for f in files_tree[2]:
            print(f"{spacer}└─ {f.name}")

    print_tree_recurse(files_tree, 0)
    print("\nTo create the actual zip, you need to specify the --output parameter")


if __name__ == "__main__":
    main()
