import json
import logging

import requests
from abc import ABC, abstractmethod
from brownie import accounts, project
from brownie.exceptions import RPCRequestError
from brownie.project.main import Project
from django.http import Http404
from mongoengine import DoesNotExist, OperationError

from ether_network import bch_connection
from utils import contract_utils, transaction_utils, base_utils
from ether_accounts.services import accounts_repository
from ether_service.settings import ERC20_CONTRACT_NAME
from contracts.models import ContractModel

logger = logging.getLogger(__name__)
_repository_ = accounts_repository.repository


class ContractRepository(ABC):

    _project_: Project = None

    def __init__(self):
        self.bch = bch_connection.bch_connection

    @abstractmethod
    def deploy(self, address_owner, token_name, token_symbol, token_supply_val):
        raise NotImplementedError

    @abstractmethod
    def contract_by_address(self, contract_address=None):
        raise NotImplementedError

    @abstractmethod
    def contracts_by_owner(self, contract_owner=None):
        raise NotImplementedError

    @abstractmethod
    def load_contract(self, contract_address=None, address_owner=None):
        raise NotImplementedError


class ContractRepositoryImpl(ContractRepository):
    def deploy(self, address_owner, token_name, token_symbol, token_supply_val, key_wallet):

        self.bch.connect()
        projects_list = project.get_loaded_projects()
        _project_ = projects_list[0]

        if key_wallet:
            address_owner = _repository_.add(key_wallet)
        erc20token = _project_[ERC20_CONTRACT_NAME]
        try:
            contract = erc20token.deploy(token_supply_val, token_name, token_symbol,
                                         {'from': address_owner}, publish_source=True)
        except Exception as exc:
            logger.exception(str(exc.args))
            raise RPCRequestError(exc.args)

        transaction = transaction_utils.transaction_receipt_handler(contract.tx)
        token_supple = base_utils.num_without_decimals(int(token_supply_val), 18)
        token_functions = contract_utils.get_functions_names_from_abi(contract.abi)
        _contract_ = contract_utils.contract_handler(contract.tx, address_owner, token_name, token_symbol,
                                                     token_supple, token_functions)

        # obj = {"username": "", "address_owner": address_owner, "contract_address": _contract_.contract_address}
        # response = requests.post(url_constants.user_service_update_user_endpoint, data=obj)
        # if not response.status_code == 200:
        #     raise Exception()

        try:
            transaction.save()
            _contract_.save()
        except Exception as exc:
            logger.exception(str(exc.args))
            raise OperationError(exc.args)
        return _contract_.to_json()

    def contract_by_address(self, contract_address=None) -> ContractModel:
        try:
            contract = ContractModel.objects.get(contract_address=contract_address)
        except DoesNotExist:
            raise Http404("No MyModel matches the given query.")
        return contract

    def contracts_by_owner(self, contract_owner=None) -> list:
        contract_addresses_list = list()
        try:
            contracts = ContractModel.objects.filter(contract_owner=contract_owner)
            for contract in contracts:
                contract_addresses_list.append(contract.contract_address)
        except DoesNotExist:
            raise Http404("No MyModel matches the given query.")
        return json.dumps(contract_addresses_list)

    def load_contract(self, contract_address=None, address_owner=None) -> str:
        self.bch.connect()
        contract = contract_utils.get_contract(address_owner, contract_address, contract_utils.EXPLORER)
        return contract.address


repository = ContractRepositoryImpl()
