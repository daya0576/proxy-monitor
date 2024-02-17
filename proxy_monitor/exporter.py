from collections import namedtuple
import time
from prometheus_client import Counter, Histogram, Summary


Label = namedtuple("Label", ["target", "proxy", "status_code", "error_msg"])
LABEL_NAMES = [x for x in Label._fields]


s = Summary("request_latency_summary", "Request latency in seconds", LABEL_NAMES)
c = Counter("request_count", "Request count", LABEL_NAMES)
h = Histogram("request_latency_seconds", "Request latency in seconds", LABEL_NAMES)


def health_counter(func):
    def wrapper(url: str, http_proxy: str = "", https_proxy: str = ""):
        resp = func(url, http_proxy=http_proxy, https_proxy=https_proxy)

        labels = Label(url, resp.proxy, resp.status_code, resp.error_message)
        c.labels(*labels).inc()

        return resp

    return wrapper


def health_summary(func):
    def wrapper(url: str, http_proxy: str = "", https_proxy: str = ""):
        start = time.time()
        resp = func(url, http_proxy=http_proxy, https_proxy=https_proxy)
        cost = time.time() - start

        labels = Label(url, resp.proxy, resp.status_code, resp.error_message)
        s.labels(*labels).observe(cost)

        return resp

    return wrapper


def health_histogram(func):
    def wrapper(url: str, http_proxy: str = "", https_proxy: str = ""):
        start = time.time()
        resp = func(url, http_proxy=http_proxy, https_proxy=https_proxy)
        cost = time.time() - start

        labels = Label(url, resp.proxy, resp.status_code, resp.error_message)
        h.labels(*labels).observe(cost)

        return resp

    return wrapper
