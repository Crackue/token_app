import json
import logging
import requests
from utils import base_utils
from telegram import Update
from telegram.ext import CallbackContext
from urllib.parse import urlunsplit
from bot_service.settings import ETHER_SERVICE_HOST, ETHER_PORT, SCHEME

logger = logging.getLogger(__name__)

ETHER_NETLOC = ETHER_SERVICE_HOST + ":" + ETHER_PORT if SCHEME == "http" else ETHER_SERVICE_HOST
ether_erc20_base = "erc20/"
ether_erc20_name = "name/"
ether_erc20_symbol = "symbol/"
ether_erc20_decimals = "decimals/"
ether_erc20_total_supply = "total_supply/"

ether_erc20_balance_of = "balance_of/"

path_name = ether_erc20_base + ether_erc20_name
path_symbol = ether_erc20_base + ether_erc20_symbol
path_decimals = ether_erc20_base + ether_erc20_decimals
path_total_supply = ether_erc20_base + ether_erc20_total_supply
path_balance_of = ether_erc20_base + ether_erc20_balance_of

ether_erc20_name_endpoint = urlunsplit((SCHEME, ETHER_NETLOC, path_name, "", ""))
ether_erc20_symbol_endpoint = urlunsplit((SCHEME, ETHER_NETLOC, path_symbol, "", ""))
ether_erc20_decimals_endpoint = urlunsplit((SCHEME, ETHER_NETLOC, path_decimals, "", ""))
ether_erc20_total_supply_endpoint = urlunsplit((SCHEME, ETHER_NETLOC, path_total_supply, "", ""))
ether_erc20_balance_of_endpoint = urlunsplit((SCHEME, ETHER_NETLOC, path_balance_of, "", ""))


def balance_of(update: Update, context: CallbackContext):
    username = update.message.from_user['username']
    is_logged_in = base_utils.is_logged_in(username)
    if not is_logged_in[0]:
        update.message.reply_text(is_logged_in[1])
        return
    obj = {"user_address": is_logged_in[1]}
    try:
        response = requests.post(ether_erc20_balance_of_endpoint, data=obj)
        resp = json.loads(response.text)
    except Exception as exc:
        logger.exception(exc)
        update.message.reply_text("FAILED! " + str(exc.args))
        return

    if resp[0]:
        update.message.reply_text("Your balance: " + str(resp[1]))
        logger.info("Balance of user " + username + ": " + str(resp[1]))
    else:
        logger.warning("Get balance_of for user " + username + " is FAILED!: " + str(resp[1]))
        update.message.reply_text("FAILED! " + str(resp[1]))
