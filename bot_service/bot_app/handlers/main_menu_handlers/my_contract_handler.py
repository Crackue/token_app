import logging

from telegram.ext import CallbackContext
from telegram.botcommandscope import BotCommandScopeChat, BotCommandScopeAllGroupChats
from telegram import Update, BotCommand
from utils import base_utils


def get_contracts_command(update: Update, context: CallbackContext) -> None:
    username = update.message.from_user['username']
    is_logged_in = base_utils.is_logged_in(username)
    if not is_logged_in[0]:
        update.message.reply_text(is_logged_in[1])
        return
