import logging
import json
import requests as http_requests
from abc import abstractmethod
from user_service_app.models import EtherUser
from user_service_app.services.repository import repository
from user_service_project.settings import ETHER_SERVICE_HOST, ETHER_PORT, SCHEME
from urllib.parse import urlunsplit

logger = logging.getLogger(__name__)

NETLOC = ETHER_SERVICE_HOST + ":" + ETHER_PORT if SCHEME == "http" else ETHER_SERVICE_HOST

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

    @abstractmethod
    def get_contracts_by_name(self, request) -> str:
        raise NotImplementedError

    @abstractmethod
    def set_contract_address_to_user(self, request) -> bool:
        raise NotImplementedError


class UserServicesRestImpl(UserServices):

    def __init__(self):
        self.repository = repository

    def signin(self, request) -> tuple:
        post = request.POST if request.POST else json.loads(request.body)
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

    def login(self, request) -> tuple:
        post = request.POST if request.POST else json.loads(request.body)
        username = post['username']
        address_owner = post['address_owner']
        password = "" # json_['password']
        key = post['key']
        obj = {"key": key}

        address = request.session.get(username)
        if not address:
            response = http_requests.post(ether_accounts_add_endpoint, data=obj)
            if not response.status_code == 200:
                logger.error(f"\n status code: {response.status_code} \n reason: {response.reason} \n url: {response.url} ")
                res = False, response.reason
                return json.dumps(res)
            logger.info("Text: " + response.text + ", url: " + response.url)
            address = response.text
            if not address and not address == 'None':
                request.session[username] = address

        if address is not None:
            if not address == address_owner:
                res = False, "This key no corresponds to user. Check your key."
                return json.dumps(res)
            user = self.repository.login(request, username, password, address_owner, True)
            if not user:
                user = EtherUser()
                user.username = username
                user.eth_addresses = address
                res = True, self.repository.signin(user).to_json()
            else:
                res = True, user.to_json()
        else:
            res = False, "address for user: " + username + " not found."
        return json.dumps(res)

    def logout(self, request):
        post = request.POST if request.POST else json.loads(request.body)
        username = post['username']
        user_address = self.repository.logout(username)
        if user_address is not None:
            response = None
            try:
                response = http_requests.get(ether_accounts_remove_endpoint + user_address)
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
        post = request.POST if request.POST else json.loads(request.body)
        user_address = post['user_address']
        obj = {"user_address": user_address}
        try:
            response = http_requests.post(ether_accounts_is_local_account_endpoint, data=obj)
            ether_response = response.text == 'True'
        except Exception as exc:
            logger.exception(exc)
            return False
        # db_response = self.repository.is_logged_in(request, user_address)

        return ether_response

    def get_user_address_by_name(self, request) -> str:
        post = request.POST if request.POST else json.loads(request.body)
        username = post['username']
        user_address = self.repository.get_user_address_by_name(request, username)
        return user_address

    def get_contracts_by_name(self, request):
        post = request.POST if request.POST else json.loads(request.body)
        username = post['username']
        user_contracts = self.repository.get_user_contracts_by_name(request, username)
        logger.info(str(user_contracts) + " contracts was retrieved fro user " + username)
        return json.dumps(user_contracts)

    def update_user(self, request) -> bool:
        post = request.POST if request.POST else json.loads(request.body)
        username = post['username']
        active_eth_address = post['active_eth_address']
        # TODO set delegation according to field
        contract_address = post['contract_address']
        response = self.repository.set_contract_address_to_user(username, active_eth_address, contract_address)
        return response


serviceRest = UserServicesRestImpl()
