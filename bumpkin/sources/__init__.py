from .base import BaseSource
from .basichttp import BasicHTTPSource

sources = {}

default_sources = [
    BasicHTTPSource
]

def setup_source(source):
    assert issubclass(source, BaseSource), f'class {source} is not based on BaseSource'
    assert sources.get(source.SOURCE_KEY) is None, f'class {source} has the samekey ({source.SOURCE_KEY}) as {sources.get(source.SOURCE_KEY)}'
    sources[source.SOURCE_KEY] = source

for default_source in default_sources:
    setup_source(default_source)

def handle_node(declaration, previous_data=dict()):
    assert typeof(declaration) == dict, 'declaration type must be a object/dictionary'
    assert typeof(previous_data) == dict, 'previous data type must be a object/dictionary'
    assert type(declaration['_type']) == str, 'declaration error: type of _type must be string'
    source_type = declaration['_type']
    assert sources.get(source_type) is not None, f'source type {source_type} is not defined or not available'
    declaration.pop('_type')
    source = sources[source_type]
    return source(**declaration).reduce(**previous_data)

def get_subcommands(subparser):
    for source_name, source in sources.items():
        def payload_fn(**kwargs):
            obj = source(**kwargs)
            print(obj.reduce())
        parser = subparser.add_parser(source_name)
        parser.set_defaults(fn=payload_fn)
        source.argparse(parser)


