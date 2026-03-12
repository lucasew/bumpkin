import logging

from ..base import BaseSource

logger = logging.getLogger(__name__)


class BasicHTTPJSONVendorSource(BaseSource):
    """
    HTTP source variant designed specifically to consume JSON endpoints directly.
    Instead of downloading a file to compute a hash, this source parses the
    response body as JSON and incorporates those keys into the bumped state.
    """

    SOURCE_KEY = "basichttpjsonvendor"

    def __init__(
        self,
        url: str,
        rehash_if_same_url=False,
        user_agent="curl/7.83.1",
        **kwargs,
    ):
        """
        Initializes the HTTP JSON vendor source.
        """
        self.url = url
        self.user_agent = user_agent
        self.rehash_if_same_url = rehash_if_same_url

    def reduce(self, **kwargs):
        """
        Fetches the JSON payload from the configured URL.

        It overwrites the entire node state with the parsed JSON dictionary
        and appends the `final_url` after any redirects.
        """
        from json import load
        from urllib import request

        ret = kwargs
        res = request.urlopen(
            request.Request(self.url, headers={"User-Agent": self.user_agent})
        )
        logger.debug(
            dict(
                url=self.url,
                rehash_if_same_url=self.rehash_if_same_url,
                user_agent=self.user_agent,
            )
        )
        ret = load(res)
        ret["final_url"] = res.url

        return ret

    @classmethod
    def argparse(cls, parser):
        parser.description = "Like basichttp but passes through the JSON content as the return value instead of instructing how to download it"  # noqa: E501
        parser.add_argument("url", type=str)
        return parser
