import logging

from telegram.ext import CallbackContext
from telegram.botcommandscope import BotCommandScopeChat, BotCommandScopeAllGroupChats
from telegram import Update, BotCommand

logger = logging.getLogger(__name__)


def command_start(update: Update, context: CallbackContext) -> None:
    logger.info(update.to_json())

    username = update.message.from_user['username']
    chat_id = update.message.chat['id']
    chat_type = update.message.chat['type']
    if chat_type == 'private':
        signin = BotCommand("signin", "sign in")
        login = BotCommand("login", "log in")
        logout = BotCommand("logout", "log out")
        balance = BotCommand("balance", "get balance(balance_of)")
        transfer = BotCommand("transfer", "transfer to")
        transfer_from = BotCommand("transfer_from", "transfer from")
        approve = BotCommand("approve", "approve withdraw to smth...")
        allowance = BotCommand("allowance", "allowance from... to...")
        commands_chat = [signin, login, logout, balance, transfer, transfer_from, approve, allowance]
        scope = BotCommandScopeChat(chat_id)
        context.bot.set_my_commands(commands_chat, timeout=None, api_kwargs=None, scope=scope)
    elif chat_type == 'group':
        bet = BotCommand("bet", "bet")
        commands_chat = [bet]
        scope_group_chat = BotCommandScopeAllGroupChats(chat_id)
        context.bot.set_my_commands(commands_chat, timeout=None, api_kwargs=None, scope=scope_group_chat)

    logger.info("Commands was set")
