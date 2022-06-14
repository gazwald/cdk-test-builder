import pytest
from aws_cdk import App, Environment  # CDKv2

# from aws_cdk.core import App, Environment  # CDKv1


@pytest.fixture(scope="session")
def stack_account() -> str:
    return "123456789012"


@pytest.fixture(scope="session")
def stack_region() -> str:
    return "ap-southeast-2"


@pytest.fixture(scope="session")
def stack_environment(stack_account, stack_region) -> Environment:
    return Environment(account=stack_account, region=stack_region)


@pytest.fixture(scope="class")
def stack_app() -> App:
    return App()
