import logging

from ..base import BaseSource

logger = logging.getLogger(__name__)


class BasicHTTPSource(BaseSource):
    SOURCE_KEY = "basichttp"

    def __init__(
        self,
        url: str,
        rehash_if_same_url=False,
        user_agent="curl/7.83.1",
        verbose=False,
        **kwargs,
    ):
        self.url = url
        self.user_agent = user_agent
        self.rehash_if_same_url = rehash_if_same_url
        self.verbose = verbose

    def reduce(self, **kwargs):
        from urllib import request

        ret = kwargs
        res = request.urlopen(
            request.Request(self.url, headers={"User-Agent": self.user_agent})
        )
        resolved_url = res.url
        logger.debug(
            dict(
                url=self.url,
                rehash_if_same_url=self.rehash_if_same_url,
                user_agent=self.user_agent,
            )
        )

        if resolved_url != ret.get("final_url") or self.rehash_if_same_url:
            logger.info(f"Downloading and hashing: {resolved_url}")
            import hashlib

            hasher = hashlib.sha256()
            while True:
                buf = res.read(16 * 1024)
                if not buf:
                    break
                hasher.update(buf)
            ret["sha256"] = hasher.hexdigest()
        ret["final_url"] = res.url
        return ret

    @classmethod
    def argparse(cls, parser):
        parser.description = "Basic fetcher for HTTP"
        parser.add_argument("url", type=str)
        parser.add_argument("-r,--rehash-if-same-url", action="store_true")
        return parser
