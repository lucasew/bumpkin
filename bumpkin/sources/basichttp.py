from .base import BaseSource

class BasicHTTPSource(BaseSource):
    def __init__(self, url: str, rehash_if_same_url=False):
        self.url = url
    def reduce(self, **kwargs):
        ret = kwargs
        from urllib import request
        import hashlib
        res = request.urlopen(request.Request(self.url))
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

