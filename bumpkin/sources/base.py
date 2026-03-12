class BaseSource:
    """
    Abstract base class for all bumpkin sources.

    A source acts as a reducer for a specific resource (like a file via HTTP or a GitHub release).
    It takes the configuration parameters and exposes a `reduce` method to compute the new state,
    comparing it against the previous state to avoid unnecessary work (e.g. refetching).
    """

    SOURCE_KEY = "_base"

    def __init__(self, **kwargs):
        """
        Initializes the source with declarative parameters from the JSON manifest.
        """
        self.kwargs = kwargs

    def reduce(self, **kwargs):
        """
        Evaluates the resource and computes the new state.

        Takes the previous state data as keyword arguments. Implementations should return
        a dictionary containing the updated state, including any new URLs or computed hashes.
        """
        raise Exception("Unimplemented")

    @classmethod
    def argparse(cls, parser):
        """
        Populates the CLI subparser with arguments specific to this source.

        Allows the source to be invoked and tested directly via the command line.
        """
        raise Exception("Unimplemented")
        return parser
