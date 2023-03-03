import logging
from typing import Optional

from .base import BaseSource

logger = logging.getLogger(__name__)

PREFIXES = [ "", "/heads", "/tags"]

class BasicGitHubSource(BaseSource):
    SOURCE_KEY = "basicgithub"

    def __init__(
        self,
        owner: str,
        repo: str,
        ref = None,
        user_agent="curl/7.83.1",
        file_type="zip",
        rehash_if_same_url=False,
        verbose=False,
        **kwargs,
    ):
        self.owner = owner
        self.repo = repo
        self.ref = ref
        self.headers = {
            "User-Agent": user_agent
        }
        self.user_agent = user_agent
        self.verbose = verbose
        self.file_type = file_type
        self.rehash_if_same_url=rehash_if_same_url

        assert file_type in ["zip", "tar.gz"], 'file type must be either zip or tar.gz'

    def _get_default_branch(self):
        from json import load
        from urllib import request
        res = request.urlopen(
            request.Request(f"https://api.github.com/repos/{self.owner}/{self.repo}", headers=self.headers)
        )
        jres = load(res)
        default_branch = jres['default_branch']
        self.ref = default_branch
        return self.ref


    def reduce(self, **kwargs):
        from urllib import request
        from json import load

        ret = kwargs

        if self.ref is None:
            if ret.get('default_branch') is None:
                ret['default_branch'] = self._get_default_branch()


        self.commit_id = None
        for prefix in PREFIXES:
            try:
                url = f"https://api.github.com/repos/{self.owner}/{self.repo}/git/matching-refs{prefix}/{self.ref}"
                print(url)
                res = request.urlopen(
                    request.Request(url, headers=self.headers)
                )
                jres = load(res)
                if len(jres) > 0:
                    obj = jres[0]['object']
                    if obj['type'] != 'commit':
                        res = request.urlopen(
                            request.Request(obj['url'], headers=self.headers)
                        )
                        jres = load(res)
                        self.commit_id = jres['object']['sha']
                    else:
                        print(obj)
                        self.commit_id = obj['sha']
            except request.HTTPError:
                continue
        assert self.commit_id is not None, f'ref {self.ref} is not valid for {self.owner}/{self.repo}'
        ret['github_commit'] = self.commit_id

        res = request.urlopen(
            request.Request(f"https://github.com/{self.owner}/{self.repo}/archive/{self.commit_id}.{self.file_type}", headers=headers)
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
        parser.add_argument("url", type=str)
        parser.add_argument("-r,--rehash-if-same-url", action="store_true")
        return parser
