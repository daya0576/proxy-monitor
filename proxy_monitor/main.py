import click
from prometheus_client import start_http_server
import time
import logging

from request import test_proxy_get

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


@click.command()
@click.option("--host", default="localhost", help="Prometheus exporter host")
@click.option("--port", default=8000, help="Prometheus exporter port")
def hello(host, port):
    logging.info("Starting Prometheus exporter on %s:%s", host, port)
    start_http_server(port, addr=host)

    # Collect metrics
    while True:
        test_proxy_get("http://wifi.vivo.com.cn/generate_204")
        test_proxy_get("http://www.google.com/generate_204")
        test_proxy_get(
            "http://www.google.com/generate_204", http_proxy="http://127.0.0.1:6152"
        )
        time.sleep(15)


if __name__ == "__main__":
    hello()
