from anyq.redis import RedisQueue
from testcontainers.redis import RedisContainer
import pytest


@pytest.fixture(scope="module")
def setup():
    redis = RedisContainer()
    redis.start()
    yield redis
    redis.stop()

def test_put(setup):
    msg = {"msg":"hello world"}
    host = setup.get_container_host_ip()
    port = setup.get_exposed_port(port=6379)
    rq = RedisQueue(host=host,port=port)
    rq.put(msg)
    assert rq.get() == msg

def test_qsize(setup):
    msg = {"msg":"hello world"}
    host = setup.get_container_host_ip()
    port = setup.get_exposed_port(port=6379)
    rq = RedisQueue(host=host,port=port)
    rq.put(msg)
    rq.put(msg)
    assert rq.qsize() == 2