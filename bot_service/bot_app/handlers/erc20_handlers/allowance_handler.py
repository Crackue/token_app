import logging
import requests
from telegram import Update
from telegram.ext import (CallbackContext, CommandHandler, MessageHandler, ConversationHandler, Filters)
from bot_service.settings import ETHER_SERVICE_HOST
from urllib.parse import urlunsplit

logger = logging.getLogger(__name__)
# _erc20_service_ = serviceBot
_erc20_service_ = 0

SCHEME = "http"
PORT = "8001"
NETLOC = ETHER_SERVICE_HOST + ":" + PORT

ether_erc20_base = "erc20/"
ether_erc20_allowance = "allowance/"
path_allowance = ether_erc20_base + ether_erc20_allowance
ether_erc20_allowance_endpoint = urlunsplit((SCHEME, NETLOC, path_allowance, "", ""))

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
    owner_name = dto['owner_name']

    obj = {"owner_name": owner_name, "spender_name": spender_name}
    response = None
    try:
        response = requests.post(ether_erc20_allowance_endpoint, data=obj)
    except Exception as exc:
        logger.exception(exc)

    _allowance_ = _erc20_service_.allowance(owner_name, spender_name)
    update.message.reply_text("Allowance: " + str(_allowance_))
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
