import os

import pytest


@pytest.fixture(scope="module")
def vcr_cassette_dir(request):
    """
    Store cassettes at tests/cassettes/{module_name}/{test_name}.yaml.

    In replay mode (default): tests run offline, zero API calls.
    To regenerate cassettes from the live API:
        pytest --record-mode=once    # record missing cassettes
        pytest --record-mode=all     # re-record everything
    """
    return os.path.join(
        os.path.dirname(str(request.fspath)),
        "cassettes",
        request.fspath.purebasename,
    )


@pytest.fixture(scope="session")
def vcr_config():
    return {
        "record_mode": "none",
        "filter_headers": ["authorization"],
    }
