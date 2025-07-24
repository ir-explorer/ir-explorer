import pytest
from testcontainers.compose import DockerCompose


@pytest.fixture(scope="module", autouse=True)
def setup(request):
    stack = DockerCompose(
        "..", ["compose.yaml", "compose.test.yaml"], build=True, wait=True
    )
    stack.start()
    request.addfinalizer(stack.stop)


@pytest.fixture(scope="module", autouse=True)
def api():
    yield "http://localhost:8203"
