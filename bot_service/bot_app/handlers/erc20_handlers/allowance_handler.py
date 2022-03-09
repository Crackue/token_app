import logging
import json
import requests
from telegram import Update
from telegram.ext import (CallbackContext, CommandHandler, MessageHandler, ConversationHandler, Filters)
from bot_service.settings import ETHER_SERVICE_HOST, ETHER_PORT, SCHEME
from urllib.parse import urlunsplit
from utils import base_utils, session_utils

logger = logging.getLogger(__name__)

ETHER_NETLOC = ETHER_SERVICE_HOST + ":" + ETHER_PORT if SCHEME == "http" else ETHER_SERVICE_HOST

ether_erc20_base = "erc20/"
ether_erc20_allowance = "allowance/"
path_allowance = ether_erc20_base + ether_erc20_allowance
ether_erc20_allowance_endpoint = urlunsplit((SCHEME, ETHER_NETLOC, path_allowance, "", ""))

OWNER_NAME, SPENDER_NAME = range(2)
dto = {}


def allowance(update: Update, context: CallbackContext):
    update.message.reply_text("Enter owner name:")
    return OWNER_NAME


def get_owner_name_allowance(update: Update, context: CallbackContext):
    owner_name = update.message['text']
    dto['owner_name'] = owner_name
    update.message.reply_text("Enter spender name:")
    return SPENDER_NAME


def get_spender_name_allowance(update: Update, context: CallbackContext):
    spender_name = update.message['text']
    address_spender = base_utils.get_user_address_by_name(spender_name)
    if not address_spender[0]:
        update.message.reply_text(address_spender[1])
        return ConversationHandler.END

    owner_name = dto['owner_name']
    address_owner = base_utils.get_user_address_by_name(owner_name)
    if not address_owner[0]:
        update.message.reply_text(address_owner[1])
        return ConversationHandler.END

    obj = {"address_owner": address_owner[1], "address_spender": address_spender[1]}
    ss = session_utils.get_session_store(update)
    try:
        session_id = ss['ether_service_session_id']
        cookies = dict(sessionid=session_id)
        response = requests.post(ether_erc20_allowance_endpoint, data=obj, cookies=cookies)
    except KeyError:
        response = requests.post(ether_erc20_allowance_endpoint, data=obj)
        session_id = response.cookies.get_dict()['sessionid']
        ss['ether_service_session_id'] = session_id
        ss.save()
    if not response.status_code == 200:
        update.message.reply_text("FAILED: " + response.reason)
        return ConversationHandler.END
    resp = json.loads(response.text)
    if resp[0]:
        update.message.reply_text("Allowance: " + str(resp[1]))
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


allowance_conv_handler = ConversationHandler(
    entry_points=[CommandHandler('allowance', allowance)],
    states={
        OWNER_NAME: [MessageHandler(Filters.reply, get_owner_name_allowance),
                     MessageHandler(Filters.text, repeat_or_stop)],
        SPENDER_NAME: [MessageHandler(Filters.reply, get_spender_name_allowance),
                       MessageHandler(Filters.text, repeat_or_stop)],
    },
    fallbacks=[MessageHandler(Filters.regex(r'stop'), cancel)],
)
