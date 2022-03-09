import logging
import json
import requests
from telegram import Update
from telegram.ext import (CallbackContext, CommandHandler, MessageHandler, ConversationHandler, Filters)
from utils.base_utils import amount_validate
from bot_service.settings import ETHER_SERVICE_HOST, ETHER_PORT, SCHEME
from urllib.parse import urlunsplit
from utils import base_utils, session_utils

logger = logging.getLogger(__name__)

ETHER_NETLOC = ETHER_SERVICE_HOST + ":" + ETHER_PORT if SCHEME == "http" else ETHER_SERVICE_HOST

ether_erc20_base = "erc20/"
ether_erc20_transfer_from = "transfer_from/"
path_transfer_from = ether_erc20_base + ether_erc20_transfer_from
ether_erc20_transfer_from_endpoint = urlunsplit((SCHEME, ETHER_NETLOC, path_transfer_from, "", ""))

SENDER_NAME, RECIPIENT_NAME, VALUE = range(3)
dto = {}


def transfer_from(update: Update, context: CallbackContext):
    update.message.reply_text("Enter sender name:")
    return SENDER_NAME


def get_sender_name(update: Update, context: CallbackContext):
    sender_name = update.message['text']
    dto['sender_name'] = sender_name
    update.message.reply_text("Enter recipient name:")
    return RECIPIENT_NAME


def get_recipient_name_tr_from(update: Update, context: CallbackContext):
    recipient_name = update.message['text']
    dto['name_recipient'] = str(recipient_name).replace('@', '', 1) \
        if str(recipient_name).startswith('@') \
        else recipient_name
    update.message.reply_text("How much?")
    return VALUE


def get_value_tr_from(update: Update, context: CallbackContext):
    amount = update.message['text']
    value = amount_validate(amount)
    if isinstance(value, str):
        update.message.reply_text(value + ". Try again")
        return VALUE

    sender_name = dto['sender_name']
    address_from = base_utils.get_user_address_by_name(sender_name)
    if not address_from[0]:
        update.message.reply_text(address_from[1])
        return ConversationHandler.END

    recipient_name = dto['recipient_name']
    address_to = base_utils.get_user_address_by_name(recipient_name)
    if not address_to[0]:
        update.message.reply_text(address_to[1])
        return ConversationHandler.END

    username = update.message.from_user['username']
    is_logged_in = base_utils.is_logged_in(username)
    if not is_logged_in[0]:
        update.message.reply_text(is_logged_in[1])
        return ConversationHandler.END

    obj = {"msg_owner": is_logged_in[1], "address_from": address_from[1], "address_to": address_to[1], "value": value}
    ss = session_utils.get_session_store(update)
    try:
        session_id = ss['ether_service_session_id']
        cookies = dict(sessionid=session_id)
        response = requests.post(ether_erc20_transfer_from_endpoint, data=obj, cookies=cookies)
    except KeyError:
        response = requests.post(ether_erc20_transfer_from_endpoint, data=obj)
        session_id = response.cookies.get_dict()['sessionid']
        ss['ether_service_session_id'] = session_id
        ss.save()
    if not response.status_code == 200:
        update.message.reply_text("FAILED!!! " + response.reason)
        return ConversationHandler.END
    resp = json.loads(response.text)
    if resp[0]:
        update.message.reply_text("Done!")
    else:
        update.message.reply_text("FAILED: " + resp[1])
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


transfer_from_conv_handler = ConversationHandler(
    entry_points=[CommandHandler('transfer_from', transfer_from)],
    states={
        SENDER_NAME: [MessageHandler(Filters.reply, get_sender_name), MessageHandler(Filters.text, repeat_or_stop)],
        RECIPIENT_NAME: [MessageHandler(Filters.reply, get_recipient_name_tr_from),
                         MessageHandler(Filters.text, repeat_or_stop)],
        VALUE: [MessageHandler(Filters.reply, get_value_tr_from), MessageHandler(Filters.text, repeat_or_stop)],
    },
    fallbacks=[MessageHandler(Filters.regex(r'stop'), cancel)],
)
