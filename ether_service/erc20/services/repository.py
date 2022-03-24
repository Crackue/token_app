import logging
from abc import ABC
from brownie import accounts
from brownie.exceptions import RPCRequestError, UnknownAccount
from mongoengine import OperationError

from ether_network import bch_connection
from erc20.services.ERC_20 import ERC_20
from utils import transaction_utils


logger = logging.getLogger(__name__)


class TokenRepository(ERC_20, ABC):

    def __init__(self):
        self.bch = bch_connection.bch_connection
        self.bch.connect()


class TokenRepositoryImpl(TokenRepository):

    def name(self, contract=None) -> str:
        return contract.name()

    def symbol(self, contract=None) -> str:
        return contract.symbol()

    def decimals(self, contract=None) -> int:
        return contract.decimals()

    def total_supply(self, contract=None) -> int:
        return contract.totalSupply()

    def balance_of(self, address_owner, contract=None):
        try:
            balance = contract.balanceOf(address_owner)
            return balance
        except Exception as exc:
            logger.exception(str(exc.args))
            raise RPCRequestError(exc.args)

    def transfer(self, address_owner, address_to, _value, contract=None) -> str:
        logger.debug("start transfer()")
        if accounts.__contains__(address_owner):
            account = accounts.at(address_owner)
        else:
            logger.warning(f"There is no address {address_owner} in ContainerAccounts")
            raise UnknownAccount(f"Probably, user {address_owner} not logged in")

        tx = contract.transfer(address_to, _value, {'from': account})
        # TODO tx.revert_msg for message error (exm: 'Insufficient Balance') or tx.trace
        transaction = transaction_utils.transaction_receipt_handler(tx)
        try:
            transaction.save()
        except Exception as exc:
            raise OperationError(exc.args)
        logger.info(tx.events)
        return str(tx.events)

    def transfer_from(self, address_owner, address_from, address_to, _value, contract=None) -> str:
        logger.debug("start transfer_from()")
        if accounts.__contains__(address_owner):
            account = accounts.at(address_owner)
        else:
            logger.warning(f"There is no address {address_owner} in ContainerAccounts")
            raise UnknownAccount(f"Probably, user {address_owner} not logged in")
        tx = contract.transferFrom(address_from, address_to, _value, {'from': account})
        transaction = transaction_utils.transaction_receipt_handler(tx)
        try:
            transaction.save()
        except Exception as exc:
            raise OperationError(exc.args)
        logger.info(tx.events)
        return str(tx.events)

    def approve(self, address_owner, address_spender, _value, contract=None) -> str:
        if accounts.__contains__(address_owner):
            account = accounts.at(address_owner)
        else:
            logger.warning(f"There is no address {address_owner} in ContainerAccounts")
            raise UnknownAccount(f"Probably, user {address_owner} not logged in")
        tx = contract.approve(address_spender, _value, {'from': account})
        transaction = transaction_utils.transaction_receipt_handler(tx)
        try:
            transaction.save()
        except Exception as exc:
            raise OperationError(exc.args)
        logger.info(tx.events)
        return str(tx.events)

    def allowance(self, address_owner, address_spender, contract=None) -> str:
        tx = contract.allowance(address_owner, address_spender)
        logger.info(tx.events)
        return str(tx.events)


repository = TokenRepositoryImpl()
