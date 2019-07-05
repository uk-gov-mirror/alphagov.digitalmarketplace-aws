
import pytest
from unittest.mock import patch

@pytest.fixture(autouse=True)
def sops_decrypt():
    with patch("deploy_tools.variables.decrypt", return_value={}) as mock:
        yield mock
