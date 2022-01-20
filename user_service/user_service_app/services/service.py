import logging
import requests
from abc import abstractmethod
from typing import Optional
from user_service_app.models import EtherUser
from user_service_app.services.repository import repository
from user_service_project.settings import ETHER_SERVICE_HOST
from urllib.parse import urlunsplit

logger = logging.getLogger(__name__)
SCHEME = "http"
PORT = "8001"
NETLOC = ETHER_SERVICE_HOST + ":" + PORT

ether_accounts_base = "accounts/"
ether_accounts_add = "add/"
ether_accounts_remove = "remove/"
ether_accounts_is_local_account = "is_local_account/"
path_add = ether_accounts_base + ether_accounts_add
path_remove = ether_accounts_base + ether_accounts_remove
path_is_local_account = ether_accounts_base + ether_accounts_is_local_account

ether_accounts_add_endpoint = urlunsplit((SCHEME, NETLOC, path_add, "", ""))
ether_accounts_remove_endpoint = urlunsplit((SCHEME, NETLOC, path_remove, "", ""))
ether_accounts_is_local_account_endpoint = urlunsplit((SCHEME, NETLOC, path_is_local_account, "", ""))


class UserServices:

    @abstractmethod
    def signin(self, request) -> tuple:
        raise NotImplementedError

    @abstractmethod
    def login(self, request) -> EtherUser:
        raise NotImplementedError

    @abstractmethod
    def logout(self, request) -> bool:
        raise NotImplementedError

    @abstractmethod
    def is_logged_in(self, request) -> bool:
        raise NotImplementedError

    @abstractmethod
    def get_user_address_by_name(self, request) -> str:
        raise NotImplementedError


class UserServicesRestImpl(UserServices):

    def __init__(self):
        self.repository = repository

    def signin(self, request) -> tuple:
        post = request.POST
        username = post['username']
        eth_address = post['eth_address']
        eth_addresses_list = [eth_address]
        eth_addresses = eth_addresses_list

        user = EtherUser()
        user.username = username
        user.eth_addresses = eth_addresses

        logger.info("Message " + str(user.to_json()))
        response = self.repository.signin(user)
        return response

    def login(self, request) -> Optional[EtherUser]:
        post = request.POST
        username = post['username']
        password = "" # json_['password']
        key = post['key']
        obj = {"key": key, "username": username}
        try:
            response = requests.post(ether_accounts_add_endpoint, data=obj)
        except Exception as exc:
            logger.exception(exc)
            return None

        # TODO more info to log
        logger.info("Text: " + response.text + ", url: " + response.url)
        address = response.text
        if address is not None:
            user = self.repository.login(request, username, password, address, True)
            return user
        else:
            return None

    def logout(self, request):
        post = request.POST
        username = post['username']
        user_address = self.repository.logout(username)
        if user_address is not None:
            response = None
            try:
                response = requests.get(ether_accounts_remove_endpoint + user_address)
            except Exception as exc:
                logger.exception(exc)
            if response:
                return username
            else:
                logger.warning("Account of user " + username + " was not removed from AccountContainer")
        else:
            logger.warning("Active eth address of User " + username + " was not removed from DB")
        return False

    def is_logged_in(self, request) -> bool:
        post = request.POST
        user_address = post['user_address']
        obj = {"user_address": user_address}
        try:
            response = requests.post(ether_accounts_is_local_account_endpoint, data=obj)
            ether_response = response.text == 'True'
        except Exception as exc:
            logger.exception(exc)
            return False
        db_response = self.repository.is_logged_in(request, user_address)

        return True if ether_response and db_response else False

    def get_user_address_by_name(self, request) -> str:
        post = request.POST
        username = post['username']
        user_address = self.repository.get_user_address_by_name(request, username)
        return user_address


serviceRest = UserServicesRestImpl()
