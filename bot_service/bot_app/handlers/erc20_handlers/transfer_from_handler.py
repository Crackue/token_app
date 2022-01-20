import logging

from telegram import Update
from telegram.ext import (CallbackContext, CommandHandler, MessageHandler, ConversationHandler, Filters)
from utils.base_utils import amount_validate
# from erc20.services.service import serviceBot

logger = logging.getLogger(__name__)
# _erc20_service_ = serviceBot
_erc20_service_ = 0
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
    dto['recipient_name'] = recipient_name
    update.message.reply_text("How much?")
    return VALUE


def get_value_tr_from(update: Update, context: CallbackContext):
    message = update.message
    amount = update.message['text']
    res = amount_validate(amount)
    if res is not None:
        update.message.reply_text(res + ". Try again")
        return ConversationHandler.END
    sender_name = dto['sender_name']
    recipient_name = dto['recipient_name']
    response = _erc20_service_.transfer_from(message, sender_name, recipient_name, amount)
    if response:
        update.message.reply_text("Done!")
    else:
        update.message.reply_text("FAILED")
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
