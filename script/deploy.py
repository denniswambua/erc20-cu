from eth_utils import to_wei
from moccasin.boa_tools import VyperContract

from contracts import snek_token

INITIAL_SUPPLY = to_wei(1000, "ether")


def deploy() -> VyperContract:
    snek_contract = snek_token(INITIAL_SUPPLY)

    print(f"Deployed to {snek_contract}")

    return snek_contract


def moccasin_main() -> VyperContract:
    return deploy()
