import json
import logging
from abc import ABC, abstractmethod

from brownie.exceptions import ContractNotFound
from brownie.network.contract import _DeployedContractBase
from erc20.services.repository import repository
from erc20.services.ERC_20 import ERC_20
from utils import base_utils, contract_utils

logger = logging.getLogger(__name__)


class TokenService(ERC_20, ABC):
    def __init__(self):
        self.repository = repository

    @abstractmethod
    def contract_info(self):
        raise NotImplementedError


class TokenServiceImpl(TokenService):

    def name(self, request) -> str:
        contract = self.retrieve_contract(request)
        _name_ = self.repository.name(contract)
        return _name_

    def symbol(self, request) -> str:
        contract = self.retrieve_contract(request)
        _symbol_ = self.repository.symbol(contract)
        return _symbol_

    def decimals(self, request) -> int:
        contract = self.retrieve_contract(request)
        _decimals_ = self.repository.decimals(contract)
        return _decimals_

    def total_supply(self, request) -> int:
        contract = self.retrieve_contract(request)
        _total_supply_ = self.repository.total_supply(contract)
        supply = base_utils.num_without_decimals(_total_supply_, 18)
        return supply

    def balance_of(self, request):
        post = request.POST if request.POST else json.loads(request.body)
        address_owner = post['address_owner']

        contract = self.retrieve_contract(request)

        _balance_of_ = self.repository.balance_of(address_owner, contract)
        # TODO 18 hardcode
        res = base_utils.num_without_decimals(_balance_of_, 18)
        return json.dumps(res)

    def transfer(self, request):
        post = request.POST if request.POST else json.loads(request.body)
        address_to = post["address_to"]
        _value_ = post["value"]
        val = base_utils.get_num_with_decimals(_value_, 18)
        address_owner = post["address_owner"]

        contract = self.retrieve_contract(request)

        _transfer_ = self.repository.transfer(address_owner, address_to, val, contract)
        return json.dumps(_transfer_)

    def transfer_from(self, request, address_from=None, address_to=None, value=None):
        post = request.POST if request.POST else json.loads(request.body)
        address_from = post["address_from"]
        address_to = post["address_to"]
        value = post["value"]
        # TODO 18 hardcode
        val = base_utils.get_num_with_decimals(value, 18)
        address_owner = post["msg_owner"]

        contract = self.retrieve_contract(request)

        _transfer_from_ = self.repository.transfer_from(address_owner, address_from, address_to, val, contract)
        return json.dumps(_transfer_from_)

    def approve(self, request):
        post = request.POST if request.POST else json.loads(request.body)
        address_spender = post["address_spender"]
        value = post["value"]
        # TODO 18 hardcode
        val = base_utils.get_num_with_decimals(value, 18)
        address_owner = post["address_owner"]

        contract = self.retrieve_contract(request)

        _approve_ = self.repository.approve(address_owner, address_spender, val, contract)
        return json.dumps(_approve_)

    def allowance(self, request):
        post = request.POST if request.POST else json.loads(request.body)
        address_spender = post["address_spender"]
        address_owner = post["address_owner"]

        contract = self.retrieve_contract(request)

        _allowance_ = self.repository.allowance(address_owner, address_spender, contract)
        if _allowance_[0]:
            value = base_utils.num_without_decimals(_allowance_[1], 18)
            allow = True, value
            return json.dumps(allow)
        return json.dumps(_allowance_)

    def contract_info(self, request):
        contract = self.retrieve_contract(request)
        _total_supply_ = self.repository.total_supply(contract)
        _contract_info_ = {
            'contract_address': contract.address,
            'token_name': self.repository.name(contract),
            'token_symbol': self.repository.symbol(contract),
            'token_decimals': str(self.repository.decimals(contract)),
            'token_supply': str(base_utils.num_without_decimals(_total_supply_, 18)),
            'token_functions': contract_utils.get_functions_names_from_abi(contract.abi)}
        return json.dumps(_contract_info_)

    @staticmethod
    def retrieve_contract(request) -> _DeployedContractBase:
        post = request.POST if request.POST else json.loads(request.body)
        address_owner = post['address_owner']
        contract_address = request.session.get(address_owner)
        if not contract_address:
            raise ContractNotFound("Contract was not loaded")
        contract = contract_utils.get_contract(contract_address)
        if not contract:
            raise ContractNotFound("Contract " + contract_address + " was not found")
        request.session[address_owner] = contract_address
        return contract


serviceRest = TokenServiceImpl()
