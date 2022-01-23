import json
import logging
from abc import ABC

from erc20.services.repository import repository
from erc20.services.ERC_20 import ERC_20
from utils import base_utils

logger = logging.getLogger(__name__)


class TokenService(ERC_20, ABC):
    def __init__(self):
        self.repository = repository


class TokenServiceImpl(TokenService):

    def name(self) -> str:
        _name_ = self.repository.name()
        return _name_

    def symbol(self) -> str:
        _symbol_ = self.repository.symbol()
        return _symbol_

    def decimals(self) -> int:
        _decimals_ = self.repository.decimals()
        return _decimals_

    def total_supply(self) -> int:
        _total_supply_ = self.repository.total_supply()
        return _total_supply_

    def balance_of(self, request) -> tuple:
        post = request.POST
        user_address = post['user_address']
        _balance_of_ = self.repository.balance_of(user_address)
        # TODO 18 hardcode
        res = True, base_utils.num_without_decimals(_balance_of_[1], 18)
        if _balance_of_[0]:
            return json.dumps(res)
        else:
            return json.dumps(_balance_of_)

    def transfer(self, request) -> tuple:
        post = request.POST
        address_to = post["address_to"]
        _value_ = post["value"]
        address_owner = post["address_owner"]
        # TODO 18 hardcode
        val = base_utils.get_num_with_decimals(_value_, 18)
        _transfer_ = self.repository.transfer(address_owner, address_to, val)
        return json.dumps(_transfer_)

    def transfer_from(self, request, address_from=None, address_to=None, value=None) -> bool:
        post = request.POST
        address_from = post["address_from"]
        address_to = post["address_to"]
        value = post["value"]
        # TODO 18 hardcode
        val = base_utils.get_num_with_decimals(value, 18)
        address_owner = post["msg_owner"]
        _transfer_from_ = self.repository.transfer_from(address_owner, address_from, address_to, val)
        return json.dumps(_transfer_from_)

    def approve(self, request) -> bool:
        post = request.POST
        address_spender = post["address_spender"]
        value = post["value"]
        # TODO 18 hardcode
        val = base_utils.get_num_with_decimals(value, 18)
        address_owner = post["address_owner"]
        _approve_ = self.repository.approve(address_owner, address_spender, val)
        return json.dumps(_approve_)

    def allowance(self, request) -> tuple:
        post = request.POST
        address_owner = post["address_owner"]
        address_spender = post["address_spender"]
        _allowance_ = self.repository.allowance(address_owner, address_spender)
        if _allowance_[0]:
            value = base_utils.num_without_decimals(_allowance_[1], 18)
            allow = True, value
            return json.dumps(allow)
        return json.dumps(_allowance_)


serviceRest = TokenServiceImpl()
