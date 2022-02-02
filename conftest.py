# pytest will look to conftest.py to set files to run before tests begin (ie fixtures)

# register all files that need to be available during tests
pytest_plugins = [
    "sbyra_src.tests.fixtures",
]
