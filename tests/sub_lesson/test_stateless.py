import pytest

from contracts.sub_lesson import stateless_fuzz_solvable
from hypothesis import given, HealthCheck, settings
from boa.test.strategies import strategy


@pytest.fixture(scope="function")
def contract():
    contract = stateless_fuzz_solvable.deploy()
    return contract


@settings(
    max_examples=1000, suppress_health_check=[HealthCheck.function_scoped_fixture]
)
@given(input_number=strategy("uint256"))
def test_always_return_input(contract, input_number):
    assert contract.always_returns_input_number(input_number) == input_number
