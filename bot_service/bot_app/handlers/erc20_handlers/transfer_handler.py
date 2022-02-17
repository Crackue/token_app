import logging
import json
import requests
from telegram import Update, Bot, Message
from telegram.ext import (CallbackContext, CommandHandler, MessageHandler, ConversationHandler, Filters)

from bot_app.models import TelegramMessage
from utils.base_utils import amount_validate
from bot_service.settings import ETHER_SERVICE_HOST, ETHER_PORT, SCHEME
from urllib.parse import urlunsplit
from utils import base_utils, bot_request_utils

logger = logging.getLogger(__name__)

ETHER_NETLOC = ETHER_SERVICE_HOST + ":" + ETHER_PORT if SCHEME == "http" else ETHER_SERVICE_HOST

ether_erc20_base = "erc20/"
ether_erc20_transfer = "transfer/"
path_transfer = ether_erc20_base + ether_erc20_transfer
ether_erc20_transfer_endpoint = urlunsplit((SCHEME, ETHER_NETLOC, path_transfer, "", ""))

RECIPIENT_NAME, VALUE = range(2)
dto = {}


def transfer(update: Update, context: CallbackContext):
    update.message.reply_text("Enter recipient name:")
    return RECIPIENT_NAME


def get_recipient_name(update: Update, context: CallbackContext):
    name_recipient = update.message['text']
    dto['name_recipient'] = str(name_recipient).replace('@', '', 1) \
        if str(name_recipient).startswith('@') \
        else name_recipient
    update.message.reply_text("Enter token value:")
    return VALUE


def get_value(update: Update, context: CallbackContext):
    amount = update.message['text']
    value = amount_validate(amount)
    if isinstance(value, str):
        update.message.reply_text(value + ". Try again")
        return VALUE

    name_recipient = dto['name_recipient']
    member = bot_request_utils.is_chat_member(update, name_recipient)
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
        logger.info(bot_request_utils.is_chat_member(context, name_recipient))
        response = requests.post(ether_erc20_transfer_endpoint, data=obj)
        resp = json.loads(response.text)
    except Exception as exc:
        logger.exception("Endpoint: " + ether_erc20_transfer_endpoint + ". Error message: " + str(exc.args))
        update.message.reply_text("Something goes wrong... Try again")
        return ConversationHandler.END
    if resp[0]:
        # TODO implement sending notification to recipient
        # message_q_set = TelegramMessage.objects.filter(message__chat__username=name_recipient)
        # message_obj = message_q_set.order_by('date_modified').first()
        # if message_obj:
        #     chat_id = message_obj['message']['chat']['id']
        #     context.bot.send_message(chat_id=chat_id,
        #                                     text="Transaction from " + username + " was complete. Check your balance")
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


transfer_conv_handler = ConversationHandler(
    entry_points=[CommandHandler('transfer', transfer)],
    states={
        RECIPIENT_NAME: [MessageHandler(Filters.reply, get_recipient_name),
                         MessageHandler(Filters.text, repeat_or_stop)],
        VALUE: [MessageHandler(Filters.reply, get_value), MessageHandler(Filters.text, repeat_or_stop)],
    },
    fallbacks=[MessageHandler(Filters.regex(r'stop'), cancel)],
)
