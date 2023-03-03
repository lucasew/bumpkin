"""CLI interface for bumpkin project.

Be creative! do whatever you want!

- Install click or typer and create a CLI app
- Use builtin argparse
- Start a web application
- Import things from your .base module
"""

def demo_subcommand(subparser):
    from .sources import get_subcommands
    get_subcommands(subparser.add_subparsers())


def main():  # pragma: no cover
    """
    The main function executes on commands:
    `python -m bumpkin` and `$ bumpkin `.

    This is your program's entry point.

    You can change this function to do whatever you want.
    Examples:
        * Run a test suite
        * Run a server
        * Do some other stuff
        * Run a command line application (Click, Typer, ArgParse)
        * List all available tasks
        * Run an application (Flask, FastAPI, Django, etc.)
    """
    from argparse import ArgumentParser
    from sys import argv
    parser = ArgumentParser()
    subparsers = parser.add_subparsers()
    demo_subcommand(subparsers.add_parser('demo'))
    args = vars(parser.parse_args())
    if args.get('fn'):
        args['fn'](**args.copy())
    else:
        parser.parse_args([*argv[1:], "--help"])
