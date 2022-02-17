import logging
import os
import brownie
from abc import ABC, abstractmethod
from brownie import accounts, project
from ether_network import bch_connection
from utils import contract_utils, transaction_utils
from pathlib import Path
from ether_service.settings import BASE_DIR
from brownie.network.contract import ContractContainer
from ether_accounts.services import accounts_repository

logger = logging.getLogger(__name__)
_repository_ = accounts_repository.repository


class ContractRepository(ABC):

    def __init__(self):
        self.bch = bch_connection.bch_connection
        self.bch.connect()

    @abstractmethod
    def deploy(self, address_owner, contract_name, contract_symbol, contract_supply_val):
        raise NotImplementedError


class ContractRepositoryImpl(ContractRepository):
    def deploy(self, address_owner, contract_name, contract_symbol, contract_supply_val):
        address_owner = _repository_.add('1c189e0df2fa16aff455447479df21a3f481e39edb6a8d6f57a07076f9418d9b')
        _projects_ = project.get_loaded_projects()
        proj = _projects_[0]
        print(type(proj))
        erc20token = proj['ERC20token']
        print(type(erc20token))
        contract = erc20token.deploy(contract_supply_val, contract_name, contract_symbol,
                                     {'from': address_owner}, publish_source=True)
        print(contract)


repository = ContractRepositoryImpl()
