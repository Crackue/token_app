import logging
import json
import requests
from telegram import Update
from telegram.ext import (CallbackContext, CommandHandler, MessageHandler, ConversationHandler, Filters)
from utils.base_utils import amount_validate
from bot_service.settings import ETHER_SERVICE_HOST, ETHER_PORT, SCHEME
from urllib.parse import urlunsplit
from utils import base_utils

logger = logging.getLogger(__name__)
CONTRACT_NAME, CONTRACT_SYMBOL, CONTRACT_SUPPLY, CONTRACT_KEY_WALLET = range(4)
dto = {}

ETHER_NETLOC = ETHER_SERVICE_HOST + ":" + ETHER_PORT if SCHEME == "http" else ETHER_SERVICE_HOST

contract_base = "contract/"
contract_deploy = "deploy/"
path_deploy = contract_base + contract_deploy
contract_deploy_endpoint = urlunsplit((SCHEME, ETHER_NETLOC, path_deploy, "", ""))


def erc20_command(update: Update, context: CallbackContext):
    username = update.message.from_user['username']
    is_logged_in = base_utils.is_logged_in(username)
    if not is_logged_in[0]:
        update.message.reply_text(is_logged_in[1])
        return ConversationHandler.END
    dto['address_owner'] = is_logged_in[1]
    update.message.reply_text("Enter contract name:")
    return CONTRACT_NAME


def contract_name(update: Update, context: CallbackContext):
    _contract_name_ = update.message['text']
    # TODO add more _contract_name_ validation
    if not _contract_name_:
        return CONTRACT_NAME
    dto['contract_name'] = _contract_name_
    update.message.reply_text("Enter contract symbol:")
    return CONTRACT_SYMBOL


def contract_symbol(update: Update, context: CallbackContext):
    _contract_symbol_ = update.message['text']
    # TODO add more _contract_symbol_ validation
    if not _contract_symbol_:
        return CONTRACT_SYMBOL
    dto['contract_symbol'] = _contract_symbol_
    update.message.reply_text("Enter contract supply:")
    return CONTRACT_SUPPLY


def contract_supply(update: Update, context: CallbackContext):
    _contract_supply_ = update.message['text']
    # TODO add more _contract_supply_ validation
    if not _contract_supply_:
        return CONTRACT_SUPPLY
    value = amount_validate(_contract_supply_)
    if isinstance(value, str):
        update.message.reply_text(value + ". Try again")
        return CONTRACT_SUPPLY
    # TODO request to deploy
    obj = {"address_owner": dto['address_owner'], "contract_name": dto['contract_name'], "contract_symbol": dto['contract_symbol'], "contract_supply": value}
    try:
        response = requests.post(contract_deploy_endpoint, data=obj)
    except Exception as exc:
        logger.exception(exc)
        update.message.reply_text("Something goes wrong... Try again")
        return ConversationHandler.END
    resp = json.loads(response.text)
    if resp[0]:
        # TODO reply contract info
        update.message.reply_text("Done!")
    else:
        update.message.reply_text("FAILED! " + resp[1])
    return ConversationHandler.END


def repeat_or_stop(update: Update, context: CallbackContext):
    _text_ = update.message['text']
    if str(_text_).lower() == 'stop':
        update.message.reply_text('Buy! See you later...')
        return ConversationHandler.END
    else:
        update.message.reply_text('You should to reply on message. If you want to finished just type \"stop\"')


def cancel(update: Update, context: CallbackContext):
    update.message.reply_text('Just try again...')
    return ConversationHandler.END


erc20_conv_handler = ConversationHandler(
    entry_points=[CommandHandler('erc20', erc20_command)],
    states={
        CONTRACT_NAME: [MessageHandler(Filters.reply, contract_name), MessageHandler(Filters.text, repeat_or_stop)],
        CONTRACT_SYMBOL: [MessageHandler(Filters.reply, contract_symbol), MessageHandler(Filters.text, repeat_or_stop)],
        CONTRACT_SUPPLY: [MessageHandler(Filters.reply, contract_supply), MessageHandler(Filters.text, repeat_or_stop)],
    },
    fallbacks=[MessageHandler(Filters.regex(r'stop'), cancel)],
)