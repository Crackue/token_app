import logging

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

