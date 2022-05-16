import json
import logging
from abc import ABC, abstractmethod
from erc20.services.ERC_20 import ERC_20
from utils import base_utils, contract_utils

from erc20.tasks import name, symbol, decimals, total_supply, balance_of, transfer, \
    transfer_from, approve, allowance, base_contract_info, error_handler

logger = logging.getLogger(__name__)


class TokenService(ERC_20, ABC):

    @abstractmethod
    def contract_info(self):
        raise NotImplementedError


class TokenServiceImpl(TokenService):

    def name(self, request=None) -> str:
        post = request.POST if request.POST else json.loads(request.body)
        address_owner = post["address_owner"]
        contract_address = request.session.get(address_owner)
        response = name.s(address_owner, contract_address).on_error(error_handler.s()).apply_async()
        return response.get()

    def symbol(self, request=None) -> str:
        post = request.POST if request.POST else json.loads(request.body)
        address_owner = post["address_owner"]
        contract_address = request.session.get(address_owner)
        response = symbol.s(address_owner, contract_address).on_error(error_handler.s()).apply_async()
        return response.get()

    def decimals(self, request=None) -> int:
        post = request.POST if request.POST else json.loads(request.body)
        address_owner = post["address_owner"]
        contract_address = request.session.get(address_owner)
        response = decimals.s(address_owner, contract_address).on_error(error_handler.s()).apply_async()
        return response.get()

    def total_supply(self, request=None) -> int:
        post = request.POST if request.POST else json.loads(request.body)
        address_owner = post["address_owner"]
        contract_address = request.session.get(address_owner)
        response = total_supply.s(address_owner, contract_address).on_error(error_handler.s()).apply_async()
        return response.get()

    def balance_of(self, request=None):
        post = request.POST if request.POST else json.loads(request.body)
        address_owner = post['address_owner']

        contract_address = request.session.get(address_owner)
        response = balance_of.s(address_owner, contract_address).on_error(error_handler.s()).apply_async()
        # TODO 18 hardcode
        res = base_utils.num_without_decimals(response.get(), 18)
        return json.dumps(res)

    def transfer(self, request=None, address_owner=None, address_to=None, _value=None):
        post = request.POST if request.POST else json.loads(request.body)
        address_to = post["address_to"]
        _value_ = post["value"]
        val = base_utils.get_num_with_decimals(_value_, 18)
        address_owner = post["address_owner"]

        contract_address = request.session.get(address_owner)
        task_id = transfer.s(contract_address, address_to, val, address_owner).on_error(error_handler.s()).apply_async()
        return json.dumps(str(task_id))

    def transfer_from(self, request=None, address_from=None, address_to=None, value=None):
        post = request.POST if request.POST else json.loads(request.body)
        address_from = post["address_from"]
        address_to = post["address_to"]
        value = post["value"]
        # TODO 18 hardcode
        val = base_utils.get_num_with_decimals(value, 18)
        address_owner = post["msg_owner"]
        contract_address = request.session.get(address_owner)
        task_id = transfer_from.s(contract_address, address_owner, address_from, address_to, val)\
            .on_error(error_handler.s()).apply_async()
        return json.dumps(str(task_id))

    def approve(self, request=None, address_owner=None, address_spender=None, value=None):
        post = request.POST if request.POST else json.loads(request.body)
        address_spender = post["address_spender"]
        value = post["value"]
        # TODO 18 hardcode
        val = base_utils.get_num_with_decimals(value, 18)
        address_owner = post["address_owner"]
        contract_address = request.session.get(address_owner)
        task_id = approve.s(contract_address, address_spender, val, address_owner)\
            .on_error(error_handler.s()).apply_async()
        return json.dumps(str(task_id))

    def allowance(self, request=None, address_owner=None, address_spender=None):
        post = request.POST if request.POST else json.loads(request.body)
        address_spender = post["address_spender"]
        address_owner = post["address_owner"]
        contract_address = request.session.get(address_owner)
        response = allowance.s(contract_address, address_owner, address_spender).on_error(
            error_handler.s()).apply_async()
        return response.get()

    def contract_info(self, request=None):
        post = request.POST if request.POST else json.loads(request.body)
        address_owner = post["address_owner"]
        contract_address = request.session.get(address_owner)
        response = base_contract_info.s(address_owner, contract_address).on_error(error_handler.s()).apply_async()
        info = response.get()

        _total_supply_ = info['total_supply']
        _contract_info_ = {
            'contract_address': info['address'],
            'token_name': info['name'],
            'token_symbol': info['symbol'],
            'token_decimals': str(info['decimals']),
            'token_supply': str(base_utils.num_without_decimals(_total_supply_, 18)),
            'token_functions': contract_utils.get_functions_names_from_abi(info['abi'])}
        return json.dumps(_contract_info_)


serviceRest = TokenServiceImpl()
