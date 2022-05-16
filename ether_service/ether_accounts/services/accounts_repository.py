import logging
from abc import abstractmethod
from brownie import accounts
from brownie.network.account import LocalAccount
from ether_network import bch_connection

logger = logging.getLogger(__name__)


class AccountsRepository:

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
    def remove(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def clear(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def is_local_account(self, user_address) -> bool:
        raise NotImplementedError


class AccountsRepositoryImpl(AccountsRepository):

    def __init__(self):
        self.bch = bch_connection.bch_connection

    def add(self, key: str) -> str:
        try:
            account = accounts.add(key)
            if not isinstance(account, LocalAccount):
                accounts.remove(account)
                account = accounts.add(key)
                logger.info(accounts.__dict__)
                return account.address
        except Exception as exc:
            logger.error(exc)
            return None
        logger.info(accounts.__dict__)
        return account.address

    def at(self):
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

    def remove(self, user_address) -> bool:
        account = accounts.at(user_address)
        if accounts.__contains__(account):
            accounts.remove(account)
            logger.info(accounts.__dict__)
            logger.info("Account " + user_address + " was successfully removed from Container")
            return True
        logger.info("Account " + user_address + " not exist in AccountContainer")
        return True

    def clear(self) -> bool:
        accounts.clear()
        if accounts.__len__() == 0:
            return True
        else:
            return False

    def is_local_account(self, user_address) -> bool:
        try:
            account = accounts.at(user_address)
            if not isinstance(account, LocalAccount):
                logger.info(accounts.__dict__)
                return False
        except Exception as exc:
            logger.error(exc)
            return False
        logger.info(accounts.__dict__)
        return True


repository = AccountsRepositoryImpl()
