import os

import pytest
from testcontainers.compose import DockerCompose

BACKEND_HOST = os.environ.get("BACKEND_HOST", "localhost")
BACKEND_PORT = os.environ.get("BACKEND_PORT", "8203")


@pytest.fixture(scope="module", autouse=True)
def setup_stack(request):
    stack = DockerCompose(
        "..", ["compose.yaml", "compose.test.yaml"], build=True, wait=True
    )
    stack.start()
    request.addfinalizer(stack.stop)


@pytest.fixture(scope="module", autouse=True)
def api():
    yield f"http://{BACKEND_HOST}:{BACKEND_PORT}"
