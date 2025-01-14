import boa

from eth_utils import to_wei
from script.deploy import INITIAL_SUPPLY, deploy
from hypothesis.stateful import RuleBasedStateMachine, rule

from contracts.sub_lesson import stateful_fuzz_solvable
from boa.test.strategies import strategy
from hypothesis import settings

RANDOM_USER = boa.env.generate_address("random_user")
BURN_AMOUNT = to_wei(50, "ether")


class SnekTokenStatefulFuzzer(RuleBasedStateMachine):

    def __init__(self):
        super().__init__()
        self.contract = deploy()

    @rule()
    def super_mint(self):
        before_amount: uint256 = self.contract.totalSupply()
        self.contract.super_mint()
        assert before_amount == self.contract.totalSupply() + to_wei(
            100, "ether"
        ), f"Expected totalSupply to increase by 100"


TestStatefulFuzzing = SnekTokenStatefulFuzzer.TestCase
TestStatefulFuzzing.settings = settings(max_examples=100, stateful_step_count=50)


def test_token_supply():
    snek_token = deploy()
    assert snek_token.totalSupply() == INITIAL_SUPPLY


def test_token_event_is_logged():
    snek_token = deploy()

    with boa.env.prank(snek_token.owner()):
        snek_token.transfer(RANDOM_USER, INITIAL_SUPPLY)
        logs = snek_token.get_logs()

        owner = logs[0].topics[0]
        assert owner == snek_token.owner()
        assert snek_token.balanceOf(RANDOM_USER) == INITIAL_SUPPLY


def test_set_minter_can_mint():
    snek_token = deploy()
    with boa.env.prank(snek_token.owner()):
        snek_token.set_minter(RANDOM_USER, True)
        assert snek_token.is_minter(RANDOM_USER)

    with boa.env.prank(RANDOM_USER):
        snek_token.mint(RANDOM_USER, INITIAL_SUPPLY)
        assert snek_token.balanceOf(RANDOM_USER) == INITIAL_SUPPLY
        assert snek_token.totalSupply() == INITIAL_SUPPLY * 2


def test_burn():
    snek_token = deploy()
    with boa.env.prank(snek_token.owner()):
        snek_token.burn(BURN_AMOUNT)
        assert snek_token.totalSupply() == INITIAL_SUPPLY - BURN_AMOUNT
