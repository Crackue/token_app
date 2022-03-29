import logging
import json
import requests
from telegram import Update
from telegram.ext import (CallbackContext, CommandHandler, MessageHandler, ConversationHandler, Filters)
from utils.base_utils import amount_validate
from constants import url_constants
from utils import base_utils

logger = logging.getLogger(__name__)
TOKEN_NAME, TOKEN_SYMBOL, TOKEN_SUPPLY = range(3)
dto = {}


def erc20_command(update: Update, context: CallbackContext):
    username = update.message.from_user['username']
    is_logged_in = base_utils.is_logged_in(username)
    if not is_logged_in[0]:
        update.message.reply_text(is_logged_in[1])
        return ConversationHandler.END
    dto['address_owner'] = is_logged_in[1]
    update.message.reply_text("Enter token name:")
    return TOKEN_NAME


def token_name(update: Update, context: CallbackContext):
    _token_name_ = update.message['text']
    # TODO add more _contract_name_ validation
    if not _token_name_:
        return TOKEN_NAME
    dto['token_name'] = _token_name_
    update.message.reply_text("Enter token symbol:")
    return TOKEN_SYMBOL


def token_symbol(update: Update, context: CallbackContext):
    _token_symbol_ = update.message['text']
    # TODO add more _contract_symbol_ validation
    if not _token_symbol_:
        return TOKEN_SYMBOL
    dto['token_symbol'] = _token_symbol_
    update.message.reply_text("Enter token supply:")
    return TOKEN_SUPPLY


def token_supply(update: Update, context: CallbackContext):
    _token_supply_ = update.message['text']
    # TODO add more _contract_supply_ validation
    if not _token_supply_:
        return TOKEN_SUPPLY
    value = amount_validate(_token_supply_)
    if isinstance(value, str):
        update.message.reply_text(value + ". Try again")
        return TOKEN_SUPPLY
    # TODO request to deploy
    obj = {"address_owner": dto['address_owner'], "token_name": dto['token_name'],
           "token_symbol": dto['token_symbol'], "token_supply": value, "key_wallet": ""}

    response = requests.post(url_constants.contract_deploy_endpoint, data=obj)

    if not response.status_code == 200:
        update.message.reply_text("FAILED!!! " + response.reason)
        return ConversationHandler.END

    resp = json.loads(response.text)
    contract_address = resp['contract_address']
    username = update.message.from_user['username']
    obj = {"username": username, "contract_address": contract_address}
    requests.post(url_constants.user_service_update_user_endpoint, data=obj)
    if not response.status_code == 200:
        update.message.reply_text("FAILED!!! " + response.reason)
        return ConversationHandler.END

    update.message.reply_text("Done!")
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
        TOKEN_NAME: [MessageHandler(Filters.reply, token_name), MessageHandler(Filters.text, repeat_or_stop)],
        TOKEN_SYMBOL: [MessageHandler(Filters.reply, token_symbol), MessageHandler(Filters.text, repeat_or_stop)],
        TOKEN_SUPPLY: [MessageHandler(Filters.reply, token_supply), MessageHandler(Filters.text, repeat_or_stop)],
    },
    fallbacks=[MessageHandler(Filters.regex(r'stop'), cancel)],
)