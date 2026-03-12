import logging

from ..base import BaseSource

logger = logging.getLogger(__name__)

PREFIXES = ["", "/heads", "/tags"]


class BasicGitHubSource(BaseSource):
    """
    Source implementation that tracks a specific GitHub repository reference
    (e.g., branch or tag) and downloads an archive of the code.

    This source discovers the latest commit hash for the reference using the
    GitHub matching-refs API, ensuring updates trigger when the ref points to a
    new commit. If a matching ref is not explicitly provided, it will fallback
    to the repository's default branch.
    """

    SOURCE_KEY = "basicgithub"

    def __init__(
        self,
        owner: str,
        repo: str,
        ref=None,
        user_agent="curl/7.83.1",
        file_type="tar.gz",
        rehash_if_same_url=False,
        **kwargs,
    ):
        """
        Initializes the GitHub source config.
        """
        self.owner = owner
        self.repo = repo
        self.ref = ref
        self.headers = {"User-Agent": user_agent}
        self.user_agent = user_agent
        self.file_type = file_type
        self.rehash_if_same_url = rehash_if_same_url

        assert file_type in [
            "zip",
            "tar.gz",
        ], "file type must be either zip or tar.gz"

    def _get_default_branch(self):
        """
        Queries the GitHub API to retrieve the default branch name of the repository.
        """
        from json import load
        from urllib import request

        url = f"https://api.github.com/repos/{self.owner}/{self.repo}"
        res = request.urlopen(request.Request(url, headers=self.headers))
        jres = load(res)
        logger.debug(url, jres)
        branch = jres["default_branch"]
        return f"heads/{branch}"

    def reduce(self, **kwargs):
        """
        Evaluates the GitHub repository's ref to find the latest commit hash.

        If the final archive URL matches the previously processed URL (unless
        `rehash_if_same_url` is True), it skips downloading and hashing to
        optimize performance. Returns updated state containing the matched commit
        hash, file type, final download URL, and sha256.
        """
        from json import load
        from urllib import request

        logger.debug(
            dict(
                owner=self.owner,
                repo=self.repo,
                ref=self.ref,
                file_type=self.file_type,
            )
        )  # noqa: E501

        ret = kwargs

        if self.ref is None:
            if ret.get("default_branch") is None:
                ret["default_branch"] = self._get_default_branch()
            self.ref = ret["default_branch"]

        assert self.ref is not None, "ref must not be None"

        self.commit_id = None
        for prefix in PREFIXES:
            try:
                url = f"https://api.github.com/repos/{self.owner}/{self.repo}/git/matching-refs{prefix}/{self.ref}"  # noqa: E501
                logger.debug(url)
                res = request.urlopen(request.Request(url, headers=self.headers))
                jres = load(res)
                if len(jres) > 0:
                    obj = jres[0]["object"]
                    if obj["type"] != "commit":
                        res = request.urlopen(
                            request.Request(obj["url"], headers=self.headers)
                        )
                        jres = load(res)
                        self.commit_id = jres["object"]["sha"]
                        break
                    else:
                        self.commit_id = obj["sha"]
                        break
            except request.HTTPError as e:
                if e.code == 404:
                    continue
                raise e
        assert self.commit_id is not None, (
            f"ref {self.ref} is not valid for {self.owner}/{self.repo}"
        )
        ret["github_commit"] = self.commit_id
        logger.info(
            f"{self.owner}/{self.repo} latest github commit for ref {self.ref} is {self.commit_id}"  # noqa: E501
        )

        res = request.urlopen(
            request.Request(
                f"https://github.com/{self.owner}/{self.repo}/archive/{self.commit_id}.{self.file_type}",  # noqa: E501
                headers=self.headers,
            )
        )
        resolved_url = res.url
        logger.debug(
            dict(
                url=resolved_url,
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
        ret["file_type"] = self.file_type
        return ret

    @classmethod
    def argparse(cls, parser):
        parser.description = "Basic fetcher for GitHub"
        parser.add_argument("owner", type=str)
        parser.add_argument("repo", type=str)
        parser.add_argument("-b,--ref", type=str)
        parser.add_argument(
            "-t,--file-type", choices=["tar.gz", "zip"], default="tar.gz"
        )
        parser.add_argument("-r,--rehash-if-same-url", action="store_true")
        return parser
