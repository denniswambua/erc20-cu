# pragma version 0.4.0

"""
@license MIT
@title snek_token
@author denniswambua
@notice This is my ERC20 token
"""
# ------------------------------------------------------------------
#                             IMPORTS
# ------------------------------------------------------------------
from ethereum.ercs import IERC20

implements: IERC20

from snekmate.auth import ownable as ow
from snekmate.tokens import erc20

initializes: ow
initializes: erc20[ownable := ow]

exports: erc20.__interface__

NAME: constant(String[24]) = "snek_token"
SYMBOL: constant(String[5]) = "SNEK"
DECIMALS: constant(uint8) = 18
EIP712_VERSION: constant(String[20]) = "1"


@deploy
def __init__(initial_supply: uint256):
    ow.__init__()
    erc20.__init__(NAME, SYMBOL, DECIMALS, NAME, EIP712_VERSION)
    erc20._mint(msg.sender, initial_supply)
