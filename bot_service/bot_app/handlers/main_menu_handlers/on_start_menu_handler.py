import logging

from telegram.ext import CallbackContext
from telegram.botcommandscope import BotCommandScopeChat, BotCommandScopeAllGroupChats
from telegram import Update, BotCommand

logger = logging.getLogger(__name__)


def command_start(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat['id']
    chat_type = update.message.chat['type']
    if chat_type == 'private':
        scope = BotCommandScopeChat(chat_id)
        list_commands = context.bot.get_my_commands(scope=scope)
        if len(list_commands):
            login = BotCommand("login", "log in")
            logout = BotCommand("logout", "log out")
            my_contracts = BotCommand("my_contracts", "get my contracts")
            create_contract = BotCommand("create_contract", "create new contract")
            interact_with_contract = BotCommand("interact_with_contract", "interact with contract")
            commands_chat = [login, logout, my_contracts, create_contract, interact_with_contract]
            context.bot.set_my_commands(commands_chat, timeout=None, api_kwargs=None, scope=scope)
    elif chat_type == 'group':
        scope_group_chat = BotCommandScopeAllGroupChats(chat_id)
        list_commands = context.bot.get_my_commands(scope=scope_group_chat)
        if len(list_commands):
            bet = BotCommand("bet", "bet")
            commands_chat = [bet]
            context.bot.set_my_commands(commands_chat, timeout=None, api_kwargs=None, scope=scope_group_chat)

    logger.info("Commands was set")
