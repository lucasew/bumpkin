import logging

logger = logging.getLogger(__name__)
logging.basicConfig()

"""CLI interface for bumpkin project.

Be creative! do whatever you want!

- Install click or typer and create a CLI app
- Use builtin argparse
- Start a web application
- Import things from your .base module
"""


def demo_subcommand(subparser):
    subparser.description = "Execute specific bump modules with specified arguments"
    from .sources import get_subcommands

    get_subcommands(subparser.add_subparsers())


def eval_subcommand(subparser):
    from pathlib import Path

    subparser.description = "Evaluate a bumpkin formatted JSON to an output"
    subparser.add_argument("-v,--verbose", dest="verbose", action="store_true")
    subparser.add_argument("-i,--input", dest="input_file", type=Path, required=True)
    subparser.add_argument("-o,--output", dest="output_file", type=Path)
    subparser.add_argument(
        "-p,--pretty",
        dest="indent",
        help="Enable JSON identations instead of minified",
        action="store_true",
    )
    subparser.add_argument(
        dest="keys",
        nargs="*",
        type=str,
        help="Bump only these keys. If ommited, bump all.",
    )

    def handle(input_file, keys, indent, output_file=None, **kwargs):
        from json import dumps, loads

        from .sources import eval_nodes

        assert input_file.exists(), f"'{input_file.resolve()}' does not exist"
        input_file_data = loads(input_file.read_text())

        if output_file is None:
            output_file = Path(str(input_file) + ".lock")
        output_file_data = None
        if output_file.exists():
            output_file_data = loads(output_file.read_text())
        processed = eval_nodes(input_file_data, output_file_data, keys)
        output_file.write_text(dumps(processed, indent=4 if indent else None))

    subparser.set_defaults(fn=handle)
    # todo implement


def list_subcommand(subparser):
    from pathlib import Path

    subparser.description = "List bumpable nodes in JSON"
    subparser.add_argument("-v,--verbose", dest="verbose", action="store_true")
    subparser.add_argument("-i,--input", dest="input_file", type=Path, required=True)
    subparser.add_argument("-o,--output", dest="output_file", type=Path)
    subparser.add_argument("-s,--show-state", dest="show_state", action="store_true")

    def handle(input_file, output_file=None, show_state=False, **kwargs):
        from json import loads

        from .sources import list_nodes

        assert input_file.exists(), f"'{input_file.resolve()}' does not exist"
        if output_file is None:
            output_file = Path(str(input_file) + ".lock")
        input_file_data = loads(input_file.read_text())
        output_file_data = None
        if output_file.exists():
            output_file_data = loads(output_file.read_text())
        nodes = list_nodes(input_file_data, output_file_data)
        node_keys = list(nodes.keys())
        node_keys.sort()
        for node in node_keys:
            if show_state:
                print(node, nodes[node])
            else:
                print(node)

    subparser.set_defaults(fn=handle)
    # todo implement


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
    demo_subcommand(subparsers.add_parser("demo"))
    eval_subcommand(subparsers.add_parser("eval"))
    list_subcommand(subparsers.add_parser("list"))
    args = vars(parser.parse_args())

    if args.get("verbose"):
        logger.root.setLevel(logging.DEBUG)
    else:
        logger.root.setLevel(logging.INFO)

    logger.debug(f"args: {args}")

    if args.get("fn"):
        args["fn"](**args.copy())
    else:
        parser.parse_args([*argv[1:], "--help"])
