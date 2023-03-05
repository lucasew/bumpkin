class BaseSource:
    SOURCE_KEY = "_base"

    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def reduce(self, **kwargs):
        raise Exception("Unimplemented")

    @classmethod
    def argparse(cls, parser):
        raise Exception("Unimplemented")
        return parser
