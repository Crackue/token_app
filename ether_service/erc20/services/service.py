import json
import logging
from abc import ABC

from erc20.services.repository import repository
from erc20.services.ERC_20 import ERC_20
from erc20.models import EtherUser
from utils import base_utils

logger = logging.getLogger(__name__)


class TokenService(ERC_20, ABC):
    def __init__(self):
        self.repository = repository


class TokenServiceImpl(TokenService):

    def name(self) -> str:
        _name_ = self.repository.name()
        return _name_

    def symbol(self) -> str:
        _symbol_ = self.repository.symbol()
        return _symbol_

    def decimals(self) -> int:
        _decimals_ = self.repository.decimals()
        return _decimals_

    def total_supply(self) -> int:
        _total_supply_ = self.repository.total_supply()
        return _total_supply_

    def balance_of(self, request) -> tuple:
        post = request.POST
        user_address = post['user_address']
        _balance_of_ = self.repository.balance_of(user_address)
        res = True, base_utils.num_without_decimals(_balance_of_[1], 18)
        if _balance_of_[0]:
            # _decimals_ = self.repository.decimals()
            # TODO 18 hardcode
            return json.dumps(res)
        else:
            return json.dumps(_balance_of_)

    def transfer(self, request, address_to=None, _value=None) -> tuple:
        post = request.POST
        name_recipient = post["name_recipient"]
        _value_ = post["value"]
        # TODO 18 hardcode
        username = post["msg_owner"]
        try:
            user = EtherUser.objects.get(username=username)
        except Exception as exc:
            logger.exception(exc)
            return False, "User " + username + " not signed in"
        try:
            recipient = EtherUser.objects.get(username=name_recipient)
            # TODO fix index
            address_to = recipient.eth_addresses[0]
        except Exception as exc:
            logger.error(exc)
            return False, "User " + recipient + " not signed in"
        # TODO 18 hardcode
        value = int(_value_)
        val = base_utils.get_num_with_decimals(value, 18)
        _transfer_ = self.repository.transfer(user, address_to, val)
        return json.dumps(_transfer_)

    def transfer_from(self, request, address_from=None, address_to=None, value=None) -> bool:
        json_ = json.loads(request.body)
        address_from = json_["address_from"]
        address_to = json_["address_to"]
        value = json_["value"]
        # TODO 18 hardcode
        val = base_utils.get_num_with_decimals(value, 18)
        username = json_["msg_owner"]
        user = request.session[username]
        if user is None:
            user = EtherUser.objects.get(username=username)
            logger.info("User " + user.username + " from DB")
        _transfer_from_ = self.repository.transfer_from(user, address_from, address_to, val)
        return _transfer_from_

    def approve(self, request, address_spender=None, value=None) -> bool:
        json_ = json.loads(request.body)
        address_spender = json_["address_spender"]

        value = json_["value"]
        val = base_utils.get_num_with_decimals(value, 18)

        username = json_["msg_owner"]
        user = request.session[username]
        if user is None:
            user = EtherUser.objects.get(username=username)
            logger.info("User " + user.username + " from DB")

        _approve_ = self.repository.approve(user, address_spender, val)
        return _approve_

    def allowance(self, request) -> int:
        post = request.POST
        address_owner = post["address_owner"]
        address_spender = post["address_spender"]
        _allowance_ = self.repository.allowance(address_owner, address_spender)
        return _allowance_


serviceRest = TokenServiceImpl()


class TokenServiceBotImpl(TokenService):

    def name(self) -> str:
        _name_ = self.repository.name()
        return _name_

    def symbol(self) -> str:
        _symbol_ = self.repository.symbol()
        return _symbol_

    def decimals(self) -> int:
        _decimals_ = self.repository.decimals()
        return _decimals_

    def total_supply(self) -> int:
        _total_supply_ = self.repository.total_supply()
        return _total_supply_

    def balance_of(self, message) -> tuple:
        logger.info("Message " + str(message))
        username = message.from_user['username']
        try:
            user = EtherUser.objects.get(username=username)
        except Exception as exc:
            logger.exception(exc)
            return False, "User " + username + " not signed in"
        _balance_of_ = self.repository.balance_of(user.active_eth_address)
        # _decimals_ = self.repository.decimals()
        # TODO 18 hardcode
        if _balance_of_[0]:
            return True, base_utils.num_without_decimals(_balance_of_[1], 18)
        else:
            return _balance_of_

    def transfer(self, message, name_recipient=None, _value=None) -> tuple:
        username = message.from_user['username']
        try:
            user = EtherUser.objects.get(username=username)
        except Exception as exc:
            logger.exception(exc)
            return False, "User " + username + " not signed in"
        try:
            recipient = EtherUser.objects.get(username=name_recipient)
            # TODO fix index
            address_to = recipient.eth_addresses[0]
        except Exception as exc:
            logger.error(exc)
            return False, "User " + recipient + " not signed in"
        # TODO 18 hardcode
        value = int(_value)
        val = base_utils.get_num_with_decimals(value, 18)
        _transfer_ = self.repository.transfer(user, address_to, val)
        return _transfer_

    def transfer_from(self, message, username_from=None, username_to=None, value=None) -> bool:
        username = message.from_user['username']
        try:
            user = EtherUser.objects.get(username=username)
        except Exception as exc:
            logger.exception(exc)
            return False, "User " + username + " not signed in"
        try:
            user_from = EtherUser.objects.get(username=username_from)
            # TODO fix index
            address_from = user_from.eth_addresses[0]
            user_to = EtherUser.objects.get(username=username_to)
            # TODO fix index
            address_to = user_to.eth_addresses[0]
        except Exception as exc:
            logger.error(exc)
            return False, "User " + username + " not signed in"
        _value_ = int(value)
        val = base_utils.get_num_with_decimals(_value_, 18)
        _transfer_from_ = self.repository.transfer_from(user, address_from, address_to, val)
        return _transfer_from_

    def approve(self, message, username_spender=None, value=None) -> tuple:
        username = message.from_user['username']
        try:
            user = EtherUser.objects.get(username=username)
        except Exception as exc:
            logger.exception(exc)
            return False, "User " + username + " not signed in"
        try:
            user_spender = EtherUser.objects.get(username=username_spender)
            # TODO fix index
            address_spender = user_spender.eth_addresses[0]
        except Exception as exc:
            logger.exception(exc)
            return False, "User " + username_spender + " not signed in"
        _value_ = int(value)
        val = base_utils.get_num_with_decimals(_value_, 18)
        _approve_ = self.repository.approve(user, address_spender, val)
        if str(_approve_[1]).__contains__('eth_sendTransaction does not exist/is not available'):
            return False, 'You should to log in'
        else:
            return _approve_

    def allowance(self, owner_name, spender_name) -> int:
        try:
            owner = EtherUser.objects.get(username=owner_name)
            # TODO fix index
            address_owner = owner.eth_addresses[0]
            spender = EtherUser.objects.get(username=spender_name)
            # TODO fix index
            address_spender = spender.eth_addresses[0]
        except Exception as exc:
            logger.error(exc)
            # TODO user not signed in
            return False
        _allowance_ = self.repository.allowance(address_owner, address_spender)
        value = int(_allowance_)
        val = base_utils.num_without_decimals(value, 18)
        return val


serviceBot = TokenServiceBotImpl()
