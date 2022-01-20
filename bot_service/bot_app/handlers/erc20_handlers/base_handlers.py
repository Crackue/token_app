import json
import logging
import requests
from telegram import Update
from telegram.ext import CallbackContext
from urllib.parse import urlunsplit
from bot_service.settings import ETHER_SERVICE_HOST
from bot_service.settings import USER_SERVICE_HOST


dto = {}

logger = logging.getLogger(__name__)
# _erc20_service_ = serviceBot
_erc20_service_ = 0

SCHEME = "http"

USER_PORT = "8000"
USER_NETLOC = USER_SERVICE_HOST + ":" + USER_PORT
user_service_base = "user/"
user_service_is_logged_in = "is_logged_in/"
user_service_get_by_name = "get_user_by_name/"
path_is_logged_in = user_service_base + user_service_is_logged_in
path_get_by_name = user_service_base + user_service_get_by_name
user_service_is_logged_in_endpoint = urlunsplit((SCHEME, USER_NETLOC, path_is_logged_in, "", ""))
user_service_get_by_name_endpoint = urlunsplit((SCHEME, USER_NETLOC, path_get_by_name, "", ""))

ETHER_PORT = "8001"
ETHER_NETLOC = ETHER_SERVICE_HOST + ":" + ETHER_PORT
ether_erc20_base = "erc20/"
ether_erc20_name = "name/"
ether_erc20_symbol = "symbol/"
ether_erc20_decimals = "decimals/"
ether_erc20_total_supply = "total_supply/"
ether_erc20_balance_of = "balance_of/"
ether_erc20_transfer = "transfer/"
ether_erc20_transfer_from = "transfer_from/"
ether_erc20_approve = "approve/"
ether_erc20_allowance = "allowance/"

path_name = ether_erc20_base + ether_erc20_name
path_symbol = ether_erc20_base + ether_erc20_symbol
path_decimals = ether_erc20_base + ether_erc20_decimals
path_total_supply = ether_erc20_base + ether_erc20_total_supply
path_balance_of = ether_erc20_base + ether_erc20_balance_of
path_transfer = ether_erc20_base + ether_erc20_transfer
path_transfer_from = ether_erc20_base + ether_erc20_transfer_from
path_approve = ether_erc20_base + ether_erc20_approve
path_allowance = ether_erc20_base + ether_erc20_allowance

ether_erc20_name_endpoint = urlunsplit((SCHEME, ETHER_NETLOC, path_name, "", ""))
ether_erc20_symbol_endpoint = urlunsplit((SCHEME, ETHER_NETLOC, path_symbol, "", ""))
ether_erc20_decimals_endpoint = urlunsplit((SCHEME, ETHER_NETLOC, path_decimals, "", ""))
ether_erc20_total_supply_endpoint = urlunsplit((SCHEME, ETHER_NETLOC, path_total_supply, "", ""))
ether_erc20_balance_of_endpoint = urlunsplit((SCHEME, ETHER_NETLOC, path_balance_of, "", ""))
ether_erc20_transfer_endpoint = urlunsplit((SCHEME, ETHER_NETLOC, path_transfer, "", ""))
ether_erc20_transfer_from_endpoint = urlunsplit((SCHEME, ETHER_NETLOC, path_transfer_from, "", ""))
ether_erc20_approve_endpoint = urlunsplit((SCHEME, ETHER_NETLOC, path_approve, "", ""))
ether_erc20_allowance_endpoint = urlunsplit((SCHEME, ETHER_NETLOC, path_allowance, "", ""))


def balance_of(update: Update, context: CallbackContext):
    username = update.message.from_user['username']
    obj = {"username": username}
    try:
        user_address = requests.post(user_service_get_by_name_endpoint, data=obj)
        if user_address.text is None:
            update.message.reply_text("User does not exist. Probably, you should to sign in")
            return
    except Exception as exc:
        logger.exception(exc)
        update.message.reply_text("Something wrong: " + str(exc.args))
        return

    obj_address = {"user_address": user_address}
    try:
        response = requests.post(user_service_is_logged_in_endpoint, data=obj_address)
        is_logged_in = response.text == 'True'
        if not is_logged_in:
            update.message.reply_text("You should be logged in for this stuff")
            return
    except Exception as exc:
        logger.exception(exc)
        update.message.reply_text("Something wrong: " + exc.args)
        return

    response = None
    try:
        response = requests.post(ether_erc20_balance_of_endpoint, data=obj_address)
    except Exception as exc:
        logger.exception(exc)
    resp = json.loads(response.text)
    if resp[0]:
        update.message.reply_text("Your balance: " + str(resp[1]))
        logger.info("Balance of user " + username + ": " + str(resp[1]))
    else:
        logger.warning("Get balance_of for user " + username + " is FAILED!: " + str(resp[1]))
        update.message.reply_text("FAILED! " + str(resp[1]))
