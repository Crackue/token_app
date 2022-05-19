import logging

from user_service_app.models import EtherUser
from mongoengine.errors import DoesNotExist

logger = logging.getLogger(__name__)


def get_user_by_name(username):
    try:
        user = EtherUser.objects.get(username=username)
    except DoesNotExist as exc:
        logger.exception(str(exc.args))
        return None
    return user


def get_user_by_active_address(active_eth_address) -> EtherUser:
    try:
        users = EtherUser.objects.filter(active_eth_address=active_eth_address)
        # TODO add warning if users > 1
    except DoesNotExist as exc:
        logger.exception(str(exc.args))
        return None
    return users[0]
