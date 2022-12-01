
import json
import logging
import os
from typing import List

from brownie.exceptions import ContractNotFound
from brownie.network.contract import _DeployedContractBase
from django.core.exceptions import RequestAborted

from brownie import Contract, accounts
from brownie.network.transaction import TransactionReceipt
from ether_service.settings import BASE_DIR
from contracts.models import ContractModel

logger = logging.getLogger(__name__)
ERC20_CONTRACT_NAME = os.getenv('ERC20_CONTRACT_NAME')
LOCAL_DB = 'local_db'
ABI = 'abi'
EXPLORER = 'explorer'


def get_contract_abi(contract_name: str):

    f = open(str(BASE_DIR) + '/ttoken/build/contracts/' + contract_name + '.json')
    json_ = json.load(f)
    logger.info("ABI of contract " + contract_name + " was retrieved")
    return json_


def load_contract_from_abi(owner_address, contract_address, contract_json):
    _abi_ = contract_json["abi"]
    _contract_name_ = contract_json["contractName"]
    _account_owner_ = accounts.at(owner_address, True)
    accounts.default = _account_owner_
    contract_ = Contract.from_abi(_contract_name_, contract_address, _abi_, _account_owner_)
    logger.info("Contract " + contract_.address + " was loaded")
    logger.info(accounts.__dict__)
    return contract_


def get_contract_from_abi(owner_address, contract_address, contract_name) -> Contract:
    try:
        contract_json = get_contract_abi(contract_name)
        _contract_ = load_contract_from_abi(owner_address, contract_address, contract_json)
        return _contract_
    except Exception as exc:
        raise RequestAborted(str(exc.args))


def get_contract_from_explorer(owner_address, contract_address) -> Contract:
    try:
        _account_owner_ = accounts.at(owner_address, True)
        _contract_ = Contract.from_explorer(contract_address, None, _account_owner_)
        return _contract_
    except Exception as exc:
        raise RequestAborted(str(exc.args))


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


def get_contract_from_local_db(contract_address) -> _DeployedContractBase:
    contract = Contract(contract_address)
    return contract


def get_contract(owner_address, contract_address, source: str) -> _DeployedContractBase:
    try:
        _contract_ = Contract(f'alias_{contract_address}')
    except ValueError as err:
        logger.warning(err.args)
        if source == LOCAL_DB:
            _contract_ = Contract(contract_address)
        elif source == EXPLORER:
            _contract_ = get_contract_from_explorer(owner_address, contract_address)
        address_0x = f'alias_{contract_address}'
        _contract_.set_alias(address_0x)
        return _contract_
    return _contract_


def retrieve_contract(request) -> _DeployedContractBase:
    post = request.POST if request.POST else json.loads(request.body)
    address_owner = post['address_owner']
    contract_address = request.session.get(address_owner)
    if not contract_address:
        raise ContractNotFound("Contract was not loaded")
    contract = get_contract_from_local_db(contract_address)
    if not contract:
        raise ContractNotFound("Contract " + contract_address + " was not found")
    request.session[address_owner] = contract_address
    return contract
