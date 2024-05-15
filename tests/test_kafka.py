from anyq.kafka import KafkaQueue
from testcontainers.kafka import KafkaContainer
import pytest


@pytest.fixture(scope="module",autouse=False)
def setup():
    kafka = KafkaContainer()
    kafka.start()
    yield kafka
    kafka.stop()

def test_put(setup):
    bootstrap_server = setup.get_bootstrap_server()
    msg = {"msg":"hello world"}
    rq = KafkaQueue(url=bootstrap_server)
    rq.put(msg)
    assert rq.get() == msg