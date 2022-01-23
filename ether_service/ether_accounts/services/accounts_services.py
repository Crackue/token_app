from abc import abstractmethod

from ether_accounts.services import accounts_repository


class AccountsServices:

    @abstractmethod
    def add(self, request, key: str) -> bool:
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

    def __init__(self):
        self.repository = accounts_repository.repository

    def add(self, request) -> str:
        post = request.POST
        key = post["key"]
        return self.repository.add(key)

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
        return self.repository.remove(user_address)

    def clear(self) -> bool:
        res = self.repository.clear()
        return res

    def is_local_account(self, request) -> bool:
        post = request.POST
        user_address = post['user_address']
        res = self.repository.is_local_account(request, user_address)
        return res


service = AccountsServicesImpl()
