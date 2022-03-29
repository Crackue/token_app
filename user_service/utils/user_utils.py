import logging

from user_service_app.models import EtherUser
from mongoengine.errors import DoesNotExist

logger = logging.getLogger(__name__)


def get_user(username):
    try:
        user = EtherUser.objects.get(username=username)
    except DoesNotExist as exc:
        logger.exception(str(exc.args))
        return None
    return user
