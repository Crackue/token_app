
import json
import logging
from typing import List

from brownie import Contract, accounts
from brownie.network.transaction import TransactionReceipt
from ether_service.settings import BASE_DIR
from contracts.models import ContractModel

logger = logging.getLogger(__name__)


def get_contract_abi(contract_name: str):

    f = open(str(BASE_DIR) + '/ttoken/build/contracts/' + contract_name + '.json')
    json_ = json.load(f)
    logger.info("ABI of contract " + contract_name + " was retrieved")
    return json_


def load_contract(owner_address, contract_address, contract_json):
    _abi_ = contract_json["abi"]
    _contract_name_ = contract_json["contractName"]
    _account_owner_ = accounts.at(owner_address, True)
    accounts.default = _account_owner_
    contract_ = Contract.from_abi(_contract_name_, contract_address, _abi_, _account_owner_)
    logger.info("Contract " + contract_.address + " was loaded")
    logger.info(accounts.__dict__)
    return contract_


def contract_handler(tx: TransactionReceipt, address_owner, token_name, token_symbol, token_supply_val, token_functions) -> ContractModel:
    contract_model = ContractModel()
    contract_model.contract_name = tx.contract_name
    contract_model.contract_address = tx.contract_address
    contract_model.contract_owner = address_owner
    contract_model.token_name = token_name
    contract_model.token_symbol = token_symbol
    contract_model.token_supply = token_supply_val
    contract_model.token_functions = token_functions
    contract_model.txid = tx.txid
    contract_model.gas_price = str(tx.gas_price)
    contract_model.gas_limit = str(tx.gas_limit)
    contract_model.gas_used = str(tx.gas_used)
    contract_model.confirmations = tx.confirmations
    contract_model.block_number = int(tx.block_number)
    contract_model.timestamp = tx.timestamp
    contract_model.logs = tx.logs
    return contract_model


def get_functions_names_from_abi(abi: List) -> List:
    functions = []
    for func in abi:
        if func['type'] == "function":
            functions.append(func['name'])
    return functions


def is_contract_exist(contract_owner, token_name) -> bool:
    contracts = ContractModel.objects.filter(contract_owner=contract_owner, token_name=token_name)
    return contracts.count() > 0

