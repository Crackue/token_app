import logging

from telegram import ChatMember
from bot_app.models import TelegramMessage

logger = logging.getLogger(__name__)


def is_chat_private(message):
    chat_type = message.json['chat']['type']
    if chat_type == 'private':
        return True


def is_chat_member_kicked(update) -> bool:
    status = update.my_chat_member.new_chat_member['status']
    username = update.my_chat_member.new_chat_member.user['username']
    if status == 'kicked':
        logger.warning("User " + username + " is kicked")
        return True
    else:
        return False


def is_bot(update) -> bool:
    if not update.message:
        _is_bot_ = update.my_chat_member.new_chat_member.user['is_bot']
        username = update.my_chat_member.new_chat_member.user['username']
        if bool(_is_bot_):
            logger.warning("User " + username + " is bot")
            return True
        else:
            return False


def get_chat_member(context, name_recipient) -> ChatMember:
    # TODO not finished
    try:
        message_q_set = TelegramMessage.objects.filter(message__chat__username=name_recipient)
        message_obj = message_q_set.order_by('date_modified').first()
        if message_obj:
            chat_id = message_obj['message']['chat']['id']
            user_id = message_obj['message']['from']['id']
            member = context.bot.get_chat_member(chat_id, user_id)
            return member if member else None
    except Exception as exc:
        logger.exception(str(exc.args))
        return None
