import pytest

from brownie import ERC20token, accounts


@pytest.fixture
def token():
    return accounts[0].deploy(ERC20token, "Test Token", "TST", 18, 1000)


def test_transfer(token):
    token.transfer(accounts[1], 100, {'from': accounts[0]})
    assert token.balanceOf(accounts[0]) == 900
