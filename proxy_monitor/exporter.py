import logging

from collections import namedtuple
from prometheus_client import Histogram


Label = namedtuple("Label", ["target", "proxy", "status_code"])
LABEL_NAMES = [x for x in Label._fields]


h = Histogram("request_latency_seconds", "Request latency in seconds", LABEL_NAMES)


def health(func):
    def wrapper(*args, **kwargs):
        url = args[0]
        http_proxy = kwargs.get("http_proxy")
        https_proxy = kwargs.get("https_proxy")

        resp = func(*args, **kwargs)

        code, cost = resp.status_code, resp.time_cost
        labels = Label(url, http_proxy or https_proxy or "", code)
        h.labels(*labels).observe(cost)

        logging.info(f"{code},{cost*1000:.0f}ms,{url},{http_proxy or https_proxy}")

        return code

    return wrapper
