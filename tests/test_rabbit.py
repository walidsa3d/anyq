from anyq.rabbit import RabbitQueue
from testcontainers.rabbitmq import RabbitMqContainer
import pytest


@pytest.fixture(scope="module",autouse=False)
def setup():
    rabbit = RabbitMqContainer(username="guest",password="guest",port=5672)
    rabbit.start()
    yield rabbit
    rabbit.stop()

def test_put(setup):
    msg = {"msg":"hello world"}
    host = setup.get_container_host_ip()
    port = setup.get_exposed_port(port=5672)
    rq = RabbitQueue(host=host,port=port, qname="first")
    rq.put(msg)
    assert rq.get() == msg