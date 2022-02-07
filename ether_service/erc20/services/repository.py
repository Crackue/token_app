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

    def transfer(self, address_owner, address_to, _value) -> tuple:
        logger.debug("start transfer()")
        try:
            if accounts.__contains__(address_owner):
                account = accounts.at(address_owner)
            else:
                logger.warning("There is no address" + str(address_owner) + " in ContainerAccounts")
                return False, "User " + str(address_owner) + " not logged in"
            tx = self._contract_.transfer(address_to, _value, {'from': account})
            # TODO tx.revert_msg for message error (exm: 'Insufficient Balance') or tx.trace
            transaction = transaction_utils.transaction_receipt_handler(tx)
            try:
                transaction.save()
            except Exception as exc:
                logger.exception(exc)
                return False, str(exc.args)
            logger.info(tx.events)
            return True, True
        except Exception as exc:
            logger.exception(exc)
            return False, str(exc.args)

    def transfer_from(self, address_owner, address_from, address_to, _value) -> tuple:
        logger.debug("start transfer_from()")
        try:
            if accounts.__contains__(address_owner):
                account = accounts.at(address_owner)
            else:
                logger.warning("There is no address " + address_owner + " in ContainerAccounts")
                return False, "There is no address " + address_owner + " in ContainerAccounts"
            result = self._contract_.transferFrom(address_from, address_to, _value, {'from': account})
            transaction = transaction_utils.transaction_receipt_handler(result)
            try:
                transaction.save()
            except Exception as exc:
                logger.exception(exc)
                return False, str(exc.args)
            logger.info(result.events)
            return True, True
        except Exception as exc:
            logger.exception(exc)
            return False, str(exc.args)

    def approve(self, address_owner, address_spender, _value) -> tuple:
        try:
            if accounts.__contains__(address_owner):
                account = accounts.at(address_owner)
            else:
                logger.warning("There is no address" + address_owner + " in ContainerAccounts")
                return False, "Address " + str(address_owner) + " not logged in"
            approve = self._contract_.approve(address_spender, _value, {'from': account})
            transaction = transaction_utils.transaction_receipt_handler(approve)
            try:
                transaction.save()
            except Exception as exc:
                logger.exception(exc)
                return False, str(exc.args)
            logger.info(approve.events)
            return True, approve.status
        except Exception as exc:
            logger.info(accounts.__dict__)
            logger.exception(exc)
            return False, str(exc.args)

    def allowance(self, address_owner, address_spender) -> tuple:
        try:
            allowance = self._contract_.allowance(address_owner, address_spender)
            return True, allowance
        except Exception as exc:
            logger.exception(exc)
            return False, str(exc.args)


repository = TokenRepositoryImpl()
