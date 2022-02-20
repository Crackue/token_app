import logging
from abc import ABC, abstractmethod
from brownie import accounts, project
from django.http import Http404
from mongoengine import DoesNotExist

from ether_network import bch_connection
from utils import contract_utils, transaction_utils, base_utils
from ether_accounts.services import accounts_repository
from ether_service.settings import ERC20_CONTRACT_NAME
from contracts.models import ContractModel
from django.shortcuts import get_object_or_404

logger = logging.getLogger(__name__)
_repository_ = accounts_repository.repository


class ContractRepository(ABC):

    def __init__(self):
        self.bch = bch_connection.bch_connection
        self.bch.connect()

    @abstractmethod
    def deploy(self, address_owner, token_name, token_symbol, token_supply_val):
        raise NotImplementedError

    @abstractmethod
    def contract_by_address(self, contract_address):
        raise NotImplementedError


class ContractRepositoryImpl(ContractRepository):
    def deploy(self, address_owner, token_name, token_symbol, token_supply_val, key_wallet):
        if key_wallet:
            address_owner = _repository_.add(key_wallet)
        _projects_ = project.get_loaded_projects()
        proj = _projects_[0]
        erc20token = proj[ERC20_CONTRACT_NAME]
        contract_utils.is_contract_exist(address_owner, token_name)
        try:
            contract = erc20token.deploy(token_supply_val, token_name, token_symbol,
                                         {'from': address_owner}, publish_source=True)
        except Exception as exc:
            logger.exception(str(exc.args))

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
            return False, str(exc.args)
        return _contract_.to_json()

    def contract_by_address(self, contract_address) -> ContractModel:
        try:
            contract = ContractModel.objects.get(contract_address=contract_address)
        except DoesNotExist:
            raise Http404("No MyModel matches the given query.")
        return contract


repository = ContractRepositoryImpl()
