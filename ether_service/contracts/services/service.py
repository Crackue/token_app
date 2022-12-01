import json
import logging
from abc import ABC, abstractmethod

from utils import base_utils, contract_utils
from brownie.exceptions import ContractExists
from contracts.tasks import deploy, load_contract, contract_by_address, contracts_by_owner, error_handler

logger = logging.getLogger(__name__)


class ContractServices(ABC):
    @abstractmethod
    def deploy(self, request):
        raise NotImplementedError

    @abstractmethod
    def contract_by_address(self, request):
        raise NotImplementedError

    @abstractmethod
    def contracts_by_owner(self, request):
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
        task_id = deploy.s(address_owner, token_name, token_symbol, token_supply_val, key_wallet)\
            .on_error(error_handler.s()).apply_async()
        return json.dumps(str(task_id))

    def contract_by_address(self, request):
        post = request.POST if request.POST else json.loads(request.body)
        contract_address = post["contract_address"]
        contract = contract_by_address.s(contract_address).on_error(error_handler.s()).apply_async()
        return contract.get()

    def contracts_by_owner(self, request):
        post = request.POST if request.POST else json.loads(request.body)
        contract_owner = post["contract_owner"]
        contract = contracts_by_owner.s(contract_owner).on_error(error_handler.s()).apply_async()
        return contract.get()

    def load_contract(self, request):
        post = request.POST if request.POST else json.loads(request.body)
        address_owner = post['address_owner']
        contract_address_new = post['contract_address']
        contract_address_old = request.session.get(address_owner)
        if not contract_address_old or not contract_address_old == contract_address_new:
            request.session[address_owner] = contract_address_new
            response = load_contract.s(contract_address_new, address_owner).on_error(error_handler.s()).apply_async()
            return response.get()
        return contract_address_old


contractService = ContractServicesImpl()
