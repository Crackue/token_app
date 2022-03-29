from typing import Callable

from bot_service.settings import ETHER_SERVICE_HOST, ETHER_PORT, SCHEME, USER_SERVICE_HOST, USER_PORT
from urllib.parse import urlunsplit

ETHER_NETLOC = ETHER_SERVICE_HOST + ":" + ETHER_PORT if SCHEME == "http" else ETHER_SERVICE_HOST
ether_erc20_base = "erc20/"
# ether_erc20_name = "name/"
# ether_erc20_symbol = "symbol/"
# ether_erc20_decimals = "decimals/"
ether_erc20_total_supply = "total_supply/"
ether_erc20_contract_info = "contract_info/"
ether_erc20_balance_of = "balance_of/"
ether_erc20_approve = "approve/"
ether_erc20_allowance = "allowance/"
ether_erc20_transfer = "transfer/"
ether_erc20_transfer_from = "transfer_from/"

# path_name = ether_erc20_base + ether_erc20_name
# path_symbol = ether_erc20_base + ether_erc20_symbol
# path_decimals = ether_erc20_base + ether_erc20_decimals
path_total_supply = ether_erc20_base + ether_erc20_total_supply
path_contract_info = ether_erc20_base + ether_erc20_contract_info
path_balance_of = ether_erc20_base + ether_erc20_balance_of
path_approve = ether_erc20_base + ether_erc20_approve
path_allowance = ether_erc20_base + ether_erc20_allowance
path_transfer = ether_erc20_base + ether_erc20_transfer
path_transfer_from = ether_erc20_base + ether_erc20_transfer_from

# ether_erc20_name_endpoint = urlunsplit((SCHEME, ETHER_NETLOC, path_name, "", ""))
# ether_erc20_symbol_endpoint = urlunsplit((SCHEME, ETHER_NETLOC, path_symbol, "", ""))
# ether_erc20_decimals_endpoint = urlunsplit((SCHEME, ETHER_NETLOC, path_decimals, "", ""))
ether_erc20_total_supply_endpoint = urlunsplit((SCHEME, ETHER_NETLOC, path_total_supply, "", ""))
ether_erc20_contract_info_endpoint = urlunsplit((SCHEME, ETHER_NETLOC, path_contract_info, "", ""))
ether_erc20_balance_of_endpoint = urlunsplit((SCHEME, ETHER_NETLOC, path_balance_of, "", ""))
ether_erc20_approve_endpoint = urlunsplit((SCHEME, ETHER_NETLOC, path_approve, "", ""))
ether_erc20_allowance_endpoint = urlunsplit((SCHEME, ETHER_NETLOC, path_allowance, "", ""))
ether_erc20_transfer_endpoint = urlunsplit((SCHEME, ETHER_NETLOC, path_transfer, "", ""))
ether_erc20_transfer_from_endpoint = urlunsplit((SCHEME, ETHER_NETLOC, path_transfer_from, "", ""))

contract_base = "contract/"
contract_deploy = "deploy/"
contract_by_address = "contract_by_address/"
load_contract = "load_contract/"

path_deploy = contract_base + contract_deploy
path_contract_by_address = contract_base + contract_by_address
path_load_contract = contract_base + load_contract

contract_deploy_endpoint = urlunsplit((SCHEME, ETHER_NETLOC, path_deploy, "", ""))
contract_by_address_endpoint = urlunsplit((SCHEME, ETHER_NETLOC, path_contract_by_address, "", ""))
load_contract_endpoint = urlunsplit((SCHEME, ETHER_NETLOC, path_load_contract, "", ""))

NETLOC = USER_SERVICE_HOST + ":" + USER_PORT if SCHEME == "http" else USER_SERVICE_HOST

user_service_base = "user/"
user_service_login = "login/"
user_service_logout = "logout/"
user_service_signin = "signin/"
user_service_update_user = "update_user/"
user_service_get_contracts = "get_contracts/"

path_login = user_service_base + user_service_login
path_logout = user_service_base + user_service_logout
path_signin = user_service_base + user_service_signin
path_update_user = user_service_base + user_service_update_user
path_get_contracts = user_service_base + user_service_get_contracts

user_service_login_endpoint = urlunsplit((SCHEME, NETLOC, path_login, "", ""))
user_service_logout_endpoint = urlunsplit((SCHEME, NETLOC, path_logout, "", ""))
user_service_signin_endpoint = urlunsplit((SCHEME, NETLOC, path_signin, "", ""))
user_service_update_user_endpoint = urlunsplit((SCHEME, NETLOC, path_update_user, "", ""))
user_service_get_contracts_endpoint = urlunsplit((SCHEME, NETLOC, path_get_contracts, "", ""))


def name() -> str:
    ether_erc20_name = "name/"
    path_name = ether_erc20_base + ether_erc20_name
    return urlunsplit((SCHEME, ETHER_NETLOC, path_name, "", ""))


def symbol() -> str:
    ether_erc20_symbol = "symbol/"
    path_symbol = ether_erc20_base + ether_erc20_symbol
    return urlunsplit((SCHEME, ETHER_NETLOC, path_symbol, "", ""))


def decimals() -> str:
    ether_erc20_decimals = "decimals/"
    path_decimals = ether_erc20_base + ether_erc20_decimals
    return urlunsplit((SCHEME, ETHER_NETLOC, path_decimals, "", ""))


