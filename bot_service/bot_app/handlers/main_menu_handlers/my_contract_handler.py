import logging
import requests
import json
from telegram.ext import CallbackContext
from telegram import Update
from constants import url_constants
from utils import handlers_utils

logger = logging.getLogger(__name__)


def get_contracts_command(update: Update, context: CallbackContext) -> None:
    username = update.message.from_user['username']

    obj = {"username": username}
    response = requests.post(url_constants.user_service_get_contracts_endpoint, data=obj)
    if not response.status_code == 200:
        update.message.reply_text("FAILED!!! " + response.reason)
        return
    resp = json.loads(response.text)
    for address in resp:
        obj = {"contract_address": address}
        response = requests.post(url_constants.contract_by_address_endpoint, data=obj)
        if not response.status_code == 200:
            update.message.reply_text("FAILED!!! " + response.reason)
            break
        else:
            contract_json = json.loads(response.text)
            contract_reply = handlers_utils.convert_contract_json_to_str_reply(contract_json)
            update.message.reply_text(contract_reply)

