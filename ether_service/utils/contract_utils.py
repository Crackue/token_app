import json
import logging
from brownie import Contract, accounts
from ether_service.settings import BASE_DIR

logger = logging.getLogger(__name__)


def get_contract_abi(contractName: str):

    f = open(str(BASE_DIR) + '/ttoken/build/contracts/' + contractName + '.json')
    json_ = json.load(f)
    logger.info("ABI of contract " + contractName + " was retrieved")
    return json_


def load_contract(owner_address, contract_address, contractJSON):
    _abi_ = contractJSON["abi"]
    _contract_name_ = contractJSON["contractName"]
    _account_owner_ = accounts.at(owner_address, True)
    accounts.default = _account_owner_
    contract_ = Contract.from_abi(_contract_name_, contract_address, _abi_, _account_owner_)
    logger.info("Contract " + contract_.address + " was loaded")
    logger.info(accounts.__dict__)
    return contract_
