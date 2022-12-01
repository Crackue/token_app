import logging
from abc import abstractmethod
import json
from ether_accounts.tasks import add, remove, clear, is_local_account, error_handler

logger = logging.getLogger(__name__)


class AccountsServices:

    @abstractmethod
    def add(self, request) -> bool:
        raise NotImplementedError

    @abstractmethod
    def at(self):
        raise NotImplementedError

    @abstractmethod
    def connect_to_clef(self):
        raise NotImplementedError

    @abstractmethod
    def disconnect_from_clef(self):
        raise NotImplementedError

    @abstractmethod
    def from_mnemonic(self):
        raise NotImplementedError

    @abstractmethod
    def load(self):
        raise NotImplementedError

    @abstractmethod
    def remove(self, username):
        raise NotImplementedError

    @abstractmethod
    def clear(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def is_local_account(self, request) -> bool:
        raise NotImplementedError


class AccountsServicesImpl(AccountsServices):

    def add(self, request) -> str:
        post = request.POST if request.POST else json.loads(request.body)
        key = post["key"]
        response = add.s(key).on_error(error_handler.s()).apply_async()
        return response.get()

    def at(self):
        # TODO
        pass

    def connect_to_clef(self):
        # TODO
        pass

    def disconnect_from_clef(self):
        # TODO
        pass

    def from_mnemonic(self):
        # TODO
        pass

    def load(self):
        # TODO
        pass

    def remove(self, user_address):
        response = remove.s(user_address).on_error(error_handler.s()).apply_async()
        return response.get()

    def clear(self) -> bool:
        response = clear.s().on_error(error_handler.s()).apply_async()
        return response.get()

    def is_local_account(self, request) -> bool:
        post = request.POST if request.POST else json.loads(request.body)
        user_address = post['user_address']
        response = is_local_account.s(user_address).on_error(error_handler.s()).apply_async()
        return response.get()


service = AccountsServicesImpl()
