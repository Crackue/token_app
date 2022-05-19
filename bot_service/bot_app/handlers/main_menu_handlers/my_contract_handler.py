import logging
import requests
import json
from telegram.ext import CallbackContext
from telegram import Update
from constants import url_constants
from utils import handlers_utils, base_utils

logger = logging.getLogger(__name__)


def get_contracts_command(update: Update, context: CallbackContext) -> None:
    username = update.message.from_user['username']
    address = base_utils.get_user_address_by_name(username)
    obj = {"contract_owner": address[1]}
    response = requests.post(url_constants.contract_by_owner_endpoint, data=obj)
    if not response.status_code == 200:
        update.message.reply_text("FAILED!!! " + response.reason)
    else:
        contracts_json = json.loads(response.text)
        for contract_json in contracts_json:
            obj = {"contract_address": contract_json}
            response = requests.post(url_constants.contract_by_address_endpoint, data=obj)
            if response.status_code == 200:
                contract_json = json.loads(response.text)
                contract_reply = handlers_utils.convert_contract_json_to_str_reply(contract_json)
                update.message.reply_text(contract_reply)
