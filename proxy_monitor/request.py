import enum
import logging
import time
import requests
from requests.exceptions import Timeout

from exporter import health_cost, health_counter
from dataclasses import dataclass

TIMEOUT = 3


@dataclass
class TestRequest:
    url: str
    http_proxy: str
    https_proxy: str


@dataclass
class TestResponse:
    status_code: int
    time_cost: float
    proxy: str


class ResponseCode(enum.Enum):
    TIMEOUT = -1
    UNKNOWN = -10


@health_cost
@health_counter
def test_proxy_get(
    url: str, http_proxy: str = "", https_proxy: str = ""
) -> TestResponse:
    time_cost = 0
    try:
        proxy = {"http": http_proxy, "https": https_proxy}
        headers = {"Connection": "close"}
        r = requests.get(url, proxies=proxy, timeout=TIMEOUT, headers=headers)
        code = r.status_code
        time_cost = r.elapsed.total_seconds()
    except Timeout:
        code = ResponseCode.TIMEOUT.value
    except Exception:
        code = ResponseCode.UNKNOWN.value

    logging.info(f"{code},{time_cost*1000:.0f}ms,{url},{http_proxy or https_proxy}")
    return TestResponse(code, time_cost, http_proxy or https_proxy or "")
