import pytest


def pytest_addoption(parser):
    parser.addoption("--rundb", action="store_true", default=False, help="run slow tests")


def pytest_configure(config):
    config.addinivalue_line("markers", "slow: mark test as slow to run")


def pytest_collection_modifyitems(config, items):
    if config.getoption("--rundb"):
        # --runslow given in cli: do not skip slow tests
        return
    skip_db = pytest.mark.skip(reason="need --rundb option to run")
    for item in items:
        if "db" in item.keywords:
            item.add_marker(skip_db)
