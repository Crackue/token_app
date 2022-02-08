from ether_accounts.models import EtherUser
from mongoengine.errors import DoesNotExist


def get_user(user_id):
    try:
        user = EtherUser.objects.get(pk=user_id)
    except DoesNotExist:
        return None
    return user
