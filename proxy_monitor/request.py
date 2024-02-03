import enum
import requests
from requests.exceptions import Timeout

from exporter import health
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


class ResponseCode(enum.Enum):
    TIMEOUT = -1
    UNKNOWN = -10


@health
def test_proxy_get(
    url: str, http_proxy: str = "", https_proxy: str = ""
) -> TestResponse:
    try:
        proxy = {"http": http_proxy, "https": https_proxy}
        headers = {"Connection": "close"}
        r = requests.get(url, proxies=proxy, timeout=TIMEOUT, headers=headers)
        return TestResponse(r.status_code, r.elapsed.total_seconds())
    except Timeout:
        return TestResponse(ResponseCode.TIMEOUT.value, TIMEOUT)
    except Exception:
        return TestResponse(ResponseCode.UNKNOWN.value, 0)
