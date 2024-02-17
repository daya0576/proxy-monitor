import enum
import logging
import requests
from requests.exceptions import Timeout

from exporter import health_histogram, health_summary, health_counter
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
    error_message: str
    time_cost: float
    proxy: str


class ResponseCode(enum.Enum):
    TIMEOUT = -1
    UNKNOWN = -10


@health_summary
@health_counter
@health_histogram
def test_proxy_get(
    url: str, http_proxy: str = "", https_proxy: str = ""
) -> TestResponse:
    time_cost = 0
    error_message = ""
    try:
        proxy = {"http": http_proxy, "https": https_proxy}
        headers = {"Connection": "close"}
        r = requests.get(url, proxies=proxy, timeout=TIMEOUT, headers=headers)
        code = r.status_code
        time_cost = r.elapsed.total_seconds()
    except Timeout:
        code = ResponseCode.TIMEOUT.value
        error_message = "timeout"
    except Exception as e:
        code = ResponseCode.UNKNOWN.value
        error_message = str(e)

    logging.info(f"{code},{time_cost*1000:.0f}ms,{url},{http_proxy or https_proxy}")
    return TestResponse(code, error_message, time_cost, http_proxy or https_proxy or "")
