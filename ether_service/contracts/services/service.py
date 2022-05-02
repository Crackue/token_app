import json
import logging
from abc import ABC, abstractmethod

from brownie import project
from utils import base_utils, contract_utils
from brownie.exceptions import ContractExists
from contracts.tasks import deploy, load_contract, contract_by_address, error_handler

logger = logging.getLogger(__name__)


class ContractServices(ABC):
    @abstractmethod
    def deploy(self, request):
        raise NotImplementedError

    @abstractmethod
    def contract_by_address(self, request):
        raise NotImplementedError

    @abstractmethod
    def load_contract(self, request):
        raise NotImplementedError


class ContractServicesImpl(ContractServices):
    def deploy(self, request):
        post = request.POST if request.POST else json.loads(request.body)
        address_owner = post["address_owner"]
        token_name = post["token_name"]
        token_symbol = post["token_symbol"]
        token_supply = post["token_supply"]
        key_wallet = post["key_wallet"]
        if contract_utils.is_contract_exist(address_owner, token_name):
            raise ContractExists("Contract of owner " + address_owner + " with name " + token_name + " is already exist")
        token_supply_val = base_utils.get_num_with_decimals(token_supply, 18)
        token_info = deploy.s(address_owner, token_name, token_symbol, token_supply_val, key_wallet)\
            .on_error(error_handler.s()).apply_async()
        return token_info

    def contract_by_address(self, request):
        post = request.POST if request.POST else json.loads(request.body)
        contract_address = post["contract_address"]
        contract = contract_by_address.s(contract_address).on_error(error_handler.s()).apply_async()
        return contract.get().to_json()

    def load_contract(self, request):
        post = request.POST if request.POST else json.loads(request.body)
        address_owner = post['address_owner']
        contract_address = request.session.get(address_owner)
        if not contract_address:
            contract_address = post['contract_address']
            request.session[address_owner] = contract_address
            response = load_contract.s(contract_address, address_owner).on_error(error_handler.s()).apply_async()
            return response.get()
        return contract_address


contractService = ContractServicesImpl()
