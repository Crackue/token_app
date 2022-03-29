import json
import logging
import requests

from utils import base_utils, session_utils
from telegram import Update
from telegram.ext import CallbackContext
from constants import url_constants

logger = logging.getLogger(__name__)


def get_contract_name(update: Update, context: CallbackContext):

    response = get_response(update, url_constants.name())
    if response is None:
        return

    resp = json.loads(response.text)
    if resp:
        update.message.reply_text(f"Contract Name: {resp}")
        logger.info(f"Contract Name: {resp}")
    else:
        logger.warning(f"Get contract name FAILED. {resp}")
        update.message.reply_text(f"Get contract name FAILED. {resp}")


def get_contract_symbol(update: Update, context: CallbackContext):
    response = get_response(update, url_constants.symbol())
    if response is None:
        return

    resp = json.loads(response.text)
    if resp:
        update.message.reply_text(f"Contract Symbol: {resp}")
        logger.info(f"Contract Symbol: {resp}")
    else:
        logger.warning(f"Get contract symbol FAILED. {resp}")
        update.message.reply_text(f"Get contract symbol FAILED. {resp}")


def get_contract_decimals(update: Update, context: CallbackContext):
    response = get_response(update, url_constants.decimals())
    if response is None:
        return

    resp = json.loads(response.text)
    if resp:
        update.message.reply_text(f"Contract Decimals: {resp}")
        logger.info(f"Contract Decimals: {resp}")
    else:
        logger.warning(f"Get contract Decimals FAILED. {resp}")
        update.message.reply_text(f"Get contract Decimals FAILED. {resp}")


def get_contract_total_supply(update: Update, context: CallbackContext):
    response = get_response(update, url_constants.ether_erc20_total_supply_endpoint)
    if response is None:
        return

    resp = json.loads(response.text)
    if resp:
        update.message.reply_text(f"Contract Total Supply: {resp}")
        logger.info(f"Contract Total Supply: {resp}")
    else:
        logger.warning(f"Get contract Total Supply FAILED. {resp}")
        update.message.reply_text(f"Get contract Total Supply FAILED. {resp}")


def get_response(update: Update, endpoint):
    username = update.message.from_user['username']
    is_logged_in = base_utils.is_logged_in(username)
    if not is_logged_in[0]:
        update.message.reply_text(is_logged_in[1])
        return None
    obj = {"address_owner": is_logged_in[1]}
    ss = session_utils.get_session_store(update)
    try:
        session_id = ss['ether_service_session_id']
        cookies = dict(sessionid=session_id)
        response = requests.post(endpoint, data=obj, cookies=cookies)
    except KeyError:
        response = requests.post(endpoint, data=obj)
        session_id = response.cookies.get_dict()['sessionid']
        ss['ether_service_session_id'] = session_id
        ss.save()

    if not response.status_code == 200:
        update.message.reply_text("FAILED! " + response.reason)
        return None

    return response
