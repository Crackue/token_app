import logging
from telegram import Update
from bot_app.models import TelegramMessage

logger = logging.getLogger(__name__)


def convert_update_to_telegram_message(update: Update) -> TelegramMessage:
    update_id = update['update_id']
    message = TelegramMessage()
    message.message = update.message.to_dict()
    message.update_id = update_id
    return message
