import logging
import requests
from django.contrib.sessions.backends.cache import SessionStore
from requests.structures import CaseInsensitiveDict
from telegram import Update
from telegram.ext import (CallbackContext, CommandHandler, MessageHandler, ConversationHandler, Filters)
from bot_app.handlers.main_menu_handlers import set_contract_functions
from constants import url_constants
from utils import base_utils, session_utils

logger = logging.getLogger(__name__)

CONTRACT_FUNCTIONS = range(1)


def set_contract_address(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Enter contract address:")
    return CONTRACT_FUNCTIONS


def set_contact_commands(update: Update, context: CallbackContext):
    username = update.message.from_user['username']
    contract_address = update.message['text']
    is_logged_in = base_utils.is_logged_in(username)
    if not is_logged_in[0]:
        update.message.reply_text(is_logged_in[1])
        return ConversationHandler.END
    obj = {"address_owner": is_logged_in[1], "contract_address": contract_address}

    ss = session_utils.get_session_store(update)
    try:
        session_id = ss['ether_service_session_id']
        cookies = dict(sessionid=session_id)
        response = requests.post(url_constants.load_contract_endpoint, data=obj, cookies=cookies)
    except KeyError:
        response = requests.post(url_constants.load_contract_endpoint, data=obj)
        session_id = response.cookies.get_dict()['sessionid']
        ss['ether_service_session_id'] = session_id
        ss.save()

    if not response.status_code == 200:
        update.message.reply_text("FAILED!!! " + response.reason)
        return ConversationHandler.END
    update.message.reply_text("Done! Press Menu")
    set_contract_functions.command_interact_with_contract(update, context)
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


interact_with_contract_handler = ConversationHandler(
    entry_points=[CommandHandler('interact_with_contract', set_contract_address)],
    states={
        CONTRACT_FUNCTIONS: [MessageHandler(Filters.reply, set_contact_commands), MessageHandler(Filters.text, repeat_or_stop)],
    },
    fallbacks=[MessageHandler(Filters.regex(r'stop'), cancel)],
)

