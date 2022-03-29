import logging
from abc import ABC, abstractmethod
from brownie import accounts, project
from brownie.exceptions import RPCRequestError
from brownie.network.contract import ProjectContract, Contract, _DeployedContractBase
from brownie.project.main import Project
from django.http import Http404
from mongoengine import DoesNotExist, OperationError

from ether_network import bch_connection
from utils import contract_utils, transaction_utils, base_utils
from ether_accounts.services import accounts_repository
from ether_service.settings import ERC20_CONTRACT_NAME
from contracts.models import ContractModel
from django.shortcuts import get_object_or_404

logger = logging.getLogger(__name__)
_repository_ = accounts_repository.repository


class ContractRepository(ABC):

    _project_: Project = None

    def __init__(self):
        self.bch = bch_connection.bch_connection
        self.bch.connect()
        projects_list = project.get_loaded_projects()
        self._project_ = projects_list[0]

    @abstractmethod
    def deploy(self, address_owner, token_name, token_symbol, token_supply_val):
        raise NotImplementedError

    @abstractmethod
    def contract_by_address(self, contract_address=None):
        raise NotImplementedError

    @abstractmethod
    def load_contract(self, contract_address=None, address_owner=None):
        raise NotImplementedError


class ContractRepositoryImpl(ContractRepository):
    def deploy(self, address_owner, token_name, token_symbol, token_supply_val, key_wallet):
        if key_wallet:
            address_owner = _repository_.add(key_wallet)
        erc20token = self._project_[ERC20_CONTRACT_NAME]
        contract_utils.is_contract_exist(address_owner, token_name)
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

    def load_contract(self, contract_address=None, address_owner=None) -> _DeployedContractBase:
        contract = None
        try:
            contract = Contract('alias_' + address_owner)
        except ValueError as err:
            logger.error(str(err.args))
        if not contract:
            try:
                contract = Contract.from_explorer(contract_address)
                user_address_0x = 'alias_' + address_owner
                contract.set_alias(user_address_0x)
            except Exception as exc:
                logger.exception(str(exc.args))
        return contract


repository = ContractRepositoryImpl()
