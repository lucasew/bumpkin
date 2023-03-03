from .base import BaseSource

class BasicHTTPSource(BaseSource):
    SOURCE_KEY = "basichttp"

    def __init__(self, url: str, rehash_if_same_url=False, user_agent="curl/7.83.1", **kwargs):
        self.url = url
        self.user_agent = user_agent

    def reduce(self, **kwargs):
        ret = kwargs
        from urllib import request
        import hashlib
        res = request.urlopen(request.Request(self.url, headers={'User-Agent': self.user_agent}))
        resolved_url = res.url
        if resolved_url != ret.get('final_url') or rehash_if_same_url:
            hasher = hashlib.sha256()
            while True:
                buf = res.read(16*1024)
                if not buf:
                    break
                hasher.update(buf)
            ret['sha256'] = hasher.hexdigest()
        ret['final_url'] = res.url
        return ret
    @classmethod
    def argparse(cls, parser):
        parser.add_argument("url", type=str)
        parser.add_argument("-r,--rehash-if-same-url", action='store_true')
        return parser
