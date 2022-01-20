import logging

from telegram import Update
from telegram.ext import (CallbackContext, CommandHandler, MessageHandler, ConversationHandler, Filters)
from utils.base_utils import amount_validate
# from erc20.services.service import serviceBot

logger = logging.getLogger(__name__)
# _erc20_service_ = serviceBot
_erc20_service_ = 0
RECIPIENT_NAME, VALUE = range(2)
dto = {}


def approve(update: Update, context: CallbackContext):
    update.message.reply_text("Enter recipient name:")
    return RECIPIENT_NAME


def get_recipient_name(update: Update, context: CallbackContext):
    name_recipient = update.message['text']
    dto['name_recipient'] = name_recipient
    update.message.reply_text("How much?")
    return VALUE


def get_value(update: Update, context: CallbackContext):
    message = update.message
    amount = update.message['text']
    res = amount_validate(amount)
    if res is not None:
        update.message.reply_text(res + ". Try again")
        return VALUE
    name_recipient = dto['name_recipient']
    response = _erc20_service_.approve(message, name_recipient, amount)
    if response[0]:
        update.message.reply_text("Done!")
    else:
        update.message.reply_text("FAILED! " + response[1])
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


approve_conv_handler = ConversationHandler(
    entry_points=[CommandHandler('approve', approve)],
    states={
        RECIPIENT_NAME: [MessageHandler(Filters.reply, get_recipient_name),
                         MessageHandler(Filters.text, repeat_or_stop)],
        VALUE: [MessageHandler(Filters.reply, get_value),
                MessageHandler(Filters.text, repeat_or_stop)],
    },
    fallbacks=[MessageHandler(Filters.regex(r'stop'), cancel)],
)
