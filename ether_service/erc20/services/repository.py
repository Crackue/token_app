import logging
import os
from abc import ABC
from brownie import accounts
from ether_network import bch_connection
from erc20.services.ERC_20 import ERC_20
from utils import contract_utils, transaction_utils


logger = logging.getLogger(__name__)
ERC20_CONTRACT_ADDRESS = os.getenv('ERC20_CONTRACT_ADDRESS')
ERC20_OWNER_ADDRESS = os.getenv('ERC20_OWNER_ADDRESS')
ERC20_CONTRACT_NAME = os.getenv('ERC20_CONTRACT_NAME')


class TokenRepository(ERC_20, ABC):

    def __init__(self):
        self.bch = bch_connection.bch_connection
        self.bch.connect()
        try:
            contract_json = contract_utils.get_contract_abi(ERC20_CONTRACT_NAME)
            self._contract_ = contract_utils.load_contract(ERC20_OWNER_ADDRESS, ERC20_CONTRACT_ADDRESS, contract_json)
        except Exception as exc:
            logger.exception(exc)


class TokenRepositoryImpl(TokenRepository):

    def name(self) -> str:
        return self._contract_.name()

    def symbol(self) -> str:
        return self._contract_.symbol()

    def decimals(self) -> int:
        return self._contract_.decimals()

    def total_supply(self) -> int:
        return self._contract_.totalSupply()

    def balance_of(self, address_owner) -> tuple:
        try:
            balance = self._contract_.balanceOf(address_owner)
            return True, balance
        except Exception as exc:
            logger.exception(exc)
            return False, str(exc.args)

    def transfer(self, user, address_to, _value) -> tuple:
        logger.debug("start transfer()")
        try:
            user_address = user.active_eth_address
            if accounts.__contains__(user_address):
                account = accounts.at(user_address)
            else:
                logger.warning("There is no address" + str(user_address) + " in ContainerAccounts")
                return False, "User " + str(user.username) + " not logged in"
            # TODO add try except in case of not logged in
            tx = self._contract_.transfer(address_to, _value, {'from': account})
            transaction = transaction_utils.transaction_receipt_handler(tx)
            try:
                transaction.save()
            except Exception as exc:
                logger.exception(exc)
            logger.info(tx.events)
            return True, True
        except Exception as exc:
            logger.exception(exc)
            return False, str(exc.args)

    def transfer_from(self, user, address_from, address_to, _value) -> bool:
        logger.debug("start transfer_from()")
        try:
            user_address = user.active_eth_address
            if accounts.__contains__(user_address):
                account = accounts.at(user_address)
            else:
                logger.warning("There is no address" + user_address + " in ContainerAccounts")
                return False
            result = self._contract_.transferFrom(address_from, address_to, _value, {'from': account})
            transaction = transaction_utils.transaction_receipt_handler(result)
            try:
                transaction.save()
            except Exception as exc:
                logger.exception(exc)
            logger.info(result.events)
            return result
        except Exception as exc:
            logger.exception(exc)
            return False

    def approve(self, user, address_spender, _value) -> tuple:
        try:
            user_address = user.active_eth_address
            if accounts.__contains__(user_address):
                account = accounts.at(user_address)
            else:
                logger.warning("There is no address" + user_address + " in ContainerAccounts")
                return False, "User " + str(user.username) + " not logged in"
            approve = self._contract_.approve(address_spender, _value, {'from': account})
            transaction = transaction_utils.transaction_receipt_handler(approve)
            try:
                transaction.save()
            except Exception as exc:
                logger.exception(exc)
            logger.info(approve.events)
            return True, approve
        except Exception as exc:
            logger.info(accounts.__dict__)
            logger.exception(exc)
            return False, str(exc.args)

    def allowance(self, address_owner, address_spender) -> int:
        try:
            # TODO tuple
            allowance = self._contract_.allowance(address_owner, address_spender)
            return allowance
        except Exception as exc:
            logger.exception(exc)


repository = TokenRepositoryImpl()
