import logging
import os
from abc import ABC, abstractmethod
from brownie import accounts, project
from ether_network import bch_connection
from utils import contract_utils, transaction_utils
from pathlib import Path
from ether_service.settings import BASE_DIR
from brownie.network.contract import ContractContainer

logger = logging.getLogger(__name__)


class ContractRepository(ABC):

    def __init__(self):
        self.bch = bch_connection.bch_connection
        self.bch.connect()

    @abstractmethod
    def deploy(self, address_owner, contract_name, contract_symbol, contract_supply_val):
        raise NotImplementedError


class ContractRepositoryImpl(ContractRepository):
    def deploy(self, address_owner, contract_name, contract_symbol, contract_supply_val):
        brownie_config_path = Path(str(BASE_DIR) + "/ttoken")
        _project_ = project.load(brownie_config_path, "TtokenProject")
        # ContractContainer.de
        project.check_for_project(brownie_config_path)

repository = ContractRepositoryImpl()
