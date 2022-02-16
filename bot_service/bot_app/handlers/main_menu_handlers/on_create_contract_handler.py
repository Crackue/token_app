import logging

from telegram.ext import CallbackContext
from telegram.botcommandscope import BotCommandScopeChat, BotCommandScopeAllGroupChats
from telegram import Update, BotCommand

logger = logging.getLogger(__name__)


def command_create_contract(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat['id']
    chat_type = update.message.chat['type']
    if chat_type == 'private':
        scope = BotCommandScopeChat(chat_id)
        list_commands = context.bot.get_my_commands(scope=scope)
        if len(list_commands):
            erc20 = BotCommand("erc20", "create contract standard ERC20")
            erc721 = BotCommand("erc721", "create contract standard ERC721")
            main_menu = BotCommand("main_menu", "back to main menu")
            commands_chat = [erc20, erc721, main_menu]
            context.bot.set_my_commands(commands_chat, timeout=None, api_kwargs=None, scope=scope)
    elif chat_type == 'group':
        scope_group_chat = BotCommandScopeAllGroupChats(chat_id)
        list_commands = context.bot.get_my_commands(scope=scope_group_chat)
        if len(list_commands):
            bet = BotCommand("bet", "bet")
            commands_chat = [bet]
            context.bot.set_my_commands(commands_chat, timeout=None, api_kwargs=None, scope=scope_group_chat)

    logger.info("Commands was set")

