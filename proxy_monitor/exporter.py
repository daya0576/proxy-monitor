from collections import namedtuple
import time
from prometheus_client import Counter, Summary


Label = namedtuple("Label", ["target", "proxy", "status_code"])
LABEL_NAMES = [x for x in Label._fields]


s = Summary("request_latency_seconds", "Request latency in seconds", LABEL_NAMES)
c = Counter("request_count", "Request count", LABEL_NAMES)


def health_counter(func):
    def wrapper(url: str, http_proxy: str = "", https_proxy: str = ""):
        resp = func(url, http_proxy=http_proxy, https_proxy=https_proxy)

        code, proxy = resp.status_code, resp.proxy
        labels = Label(url, proxy, code)
        c.labels(*labels).inc()

        return resp

    return wrapper


def health_cost(func):
    def wrapper(url: str, http_proxy: str = "", https_proxy: str = ""):
        start = time.time()
        resp = func(url, http_proxy=http_proxy, https_proxy=https_proxy)
        cost = time.time() - start

        code, proxy = resp.status_code, resp.proxy
        labels = Label(url, proxy, code)
        s.labels(*labels).observe(cost)

        return resp

    return wrapper
