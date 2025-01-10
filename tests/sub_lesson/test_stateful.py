from hypothesis.stateful import RuleBasedStateMachine, rule

from contracts.sub_lesson import stateful_fuzz_solvable
from boa.test.strategies import strategy
from hypothesis import settings


class StatefulFuzzer(RuleBasedStateMachine):

    def __init__(self):
        super().__init__()
        self.contract = stateful_fuzz_solvable.deploy()

    @rule(input=strategy("uint256"))
    def change_number(self, input):
        self.contract.change_number(input)

    @rule(input=strategy("uint256"))
    def input_number_returns_itself(self, input):
        response = self.contract.always_returns_input_number(input)
        assert response == input, f"Expected {input}, got {response}"


TestStatefulFuzzing = StatefulFuzzer.TestCase
TestStatefulFuzzing.settings = settings(max_examples=100, stateful_step_count=50)
