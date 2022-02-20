
import logging

from django.contrib.auth.backends import BaseBackend
from django.core.exceptions import PermissionDenied
from user_service_app.models import EtherUser
from mongoengine.queryset.base import BaseQuerySet





class MyModelBackend(BaseBackend):

    def authenticate(self, request, username, password) -> EtherUser:
        # TODO password validation
        try:
            user = EtherUser.objects.get(username=username)
            if user is not None:
                return user
            else:
                return None
        except Exception as exc:
            logger.warning("User " + username + " does not exist. " + str(exc))
            return None
