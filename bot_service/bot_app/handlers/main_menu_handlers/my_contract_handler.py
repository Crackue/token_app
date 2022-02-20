import logging
import requests
import json
from telegram.ext import CallbackContext
from telegram.botcommandscope import BotCommandScopeChat, BotCommandScopeAllGroupChats
from telegram import Update, BotCommand
from utils import base_utils
from bot_service.settings import USER_SERVICE_HOST, USER_PORT, SCHEME
from bot_service.settings import ETHER_SERVICE_HOST, ETHER_PORT
from urllib.parse import urlunsplit
from utils import handlers_utils

logger = logging.getLogger(__name__)

ETHER_NETLOC = ETHER_SERVICE_HOST + ":" + ETHER_PORT if SCHEME == "http" else ETHER_SERVICE_HOST

contract_base = "contract/"
contract_by_address = "contract_by_address/"
path_contract_by_address = contract_base + contract_by_address
contract_by_address_endpoint = urlunsplit((SCHEME, ETHER_NETLOC, path_contract_by_address, "", ""))

NETLOC = USER_SERVICE_HOST + ":" + USER_PORT if SCHEME == "http" else USER_SERVICE_HOST

user_service_base = "user/"
user_service_get_contracts = "get_contracts/"
path_get_contracts = user_service_base + user_service_get_contracts
user_service_get_contracts_endpoint = urlunsplit((SCHEME, NETLOC, path_get_contracts, "", ""))


def get_contracts_command(update: Update, context: CallbackContext) -> None:
    username = update.message.from_user['username']

    obj = {"username": username}
    response = requests.post(user_service_get_contracts_endpoint, data=obj)
    if not response.status_code == 200:
        update.message.reply_text("FAILED!!! " + response.reason)
        return
    resp = json.loads(response.text)
    for address in resp:
        obj = {"contract_address": address}
        response = requests.post(contract_by_address_endpoint, data=obj)
        if not response.status_code == 200:
            update.message.reply_text("FAILED!!! " + response.reason)
            break
        else:
            contract_json = json.loads(response.text)
            contract_reply = handlers_utils.convert_contract_json_to_str_reply(contract_json)
            update.message.reply_text(contract_reply)

