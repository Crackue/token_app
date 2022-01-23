import logging
import json
import requests
from telegram import Update
from telegram.ext import (CallbackContext, CommandHandler, MessageHandler, ConversationHandler, Filters)
from utils.base_utils import amount_validate
from bot_service.settings import ETHER_SERVICE_HOST
from urllib.parse import urlunsplit
from utils import base_utils

logger = logging.getLogger(__name__)

SCHEME = "http"
PORT = "8001"
NETLOC = ETHER_SERVICE_HOST + ":" + PORT

ether_erc20_base = "erc20/"
ether_erc20_transfer = "transfer/"
path_transfer = ether_erc20_base + ether_erc20_transfer
ether_erc20_transfer_endpoint = urlunsplit((SCHEME, NETLOC, path_transfer, "", ""))

RECIPIENT_NAME, VALUE = range(2)
dto = {}


def transfer(update: Update, context: CallbackContext):
    update.message.reply_text("Enter recipient name:")
    return RECIPIENT_NAME


def get_recipient_name(update: Update, context: CallbackContext):
    name_recipient = update.message['text']
    dto['name_recipient'] = name_recipient
    update.message.reply_text("Enter token value:")
    return VALUE


def get_value(update: Update, context: CallbackContext):
    amount = update.message['text']
    value = amount_validate(amount)
    if isinstance(value, str):
        update.message.reply_text(value + ". Try again")
        return VALUE

    name_recipient = dto['name_recipient']
    address_to = base_utils.get_user_address_by_name(name_recipient)
    if not address_to[0]:
        update.message.reply_text(address_to[1])
        return ConversationHandler.END

    username = update.message.from_user['username']
    is_logged_in = base_utils.is_logged_in(username)
    if not is_logged_in[0]:
        update.message.reply_text(is_logged_in[1])
        return ConversationHandler.END

    obj = {"address_owner": is_logged_in[1], "address_to": address_to[1], "value": value}
    try:
        response = requests.post(ether_erc20_transfer_endpoint, data=obj)
    except Exception as exc:
        logger.exception(exc)
        update.message.reply_text("Something goes wrong... Try again")
        return ConversationHandler.END
    resp = json.loads(response.text)
    if resp[0]:
        update.message.reply_text("Done!")
    else:
        update.message.reply_text("FAILED: " + resp[1])
    return ConversationHandler.END


def repeat_or_stop(update: Update, context: CallbackContext):
    _text_ = update.message['text']
    if _text_ == 'stop':
        update.message.reply_text('Buy! See you later...')
        return ConversationHandler.END
    else:
        update.message.reply_text('You should to reply on message. If you want to finished just type \"stop\"')


def cancel(update: Update, context: CallbackContext):
    update.message.reply_text('Just try again...')
    return ConversationHandler.END


transfer_conv_handler = ConversationHandler(
    entry_points=[CommandHandler('transfer', transfer)],
    states={
        RECIPIENT_NAME: [MessageHandler(Filters.reply, get_recipient_name),
                         MessageHandler(Filters.text, repeat_or_stop)],
        VALUE: [MessageHandler(Filters.reply, get_value), MessageHandler(Filters.text, repeat_or_stop)],
    },
    fallbacks=[MessageHandler(Filters.regex(r'stop'), cancel)],
)
