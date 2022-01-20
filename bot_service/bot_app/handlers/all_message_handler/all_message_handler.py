import logging
from telegram import Update
from telegram.ext import CallbackContext

logger = logging.getLogger(__name__)


def handle_message(update: Update, context: CallbackContext):
    logger.info("handle all message")
    pass


def handle_message_reply(update: Update, context: CallbackContext):
    logger.info("Reply update " + update.to_json())
    replied_message = update.message.reply_to_message
    text = replied_message['text']
    if str(text).__contains__("Enter your wallet key"):
        answer = update.message['text']
        logger.info(answer)

