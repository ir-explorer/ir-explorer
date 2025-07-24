import pytest
import requests
from testcontainers.compose import DockerCompose

stack = DockerCompose(
    "..", ["compose.yaml", "compose.test.yaml"], build=True, wait=True
)


@pytest.fixture(scope="module", autouse=True)
def setup(request):
    stack.start()
    request.addfinalizer(stack.stop)


def test_languages():
    x = requests.get("http://localhost:8203/get_available_languages")
    assert x.json() == ["English"]
