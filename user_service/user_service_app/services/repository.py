import logging
import datetime
from abc import abstractmethod
from django.contrib.auth import authenticate
from user_service_app.models import EtherUser
from utils import user_utils

logger = logging.getLogger(__name__)


class UserRepository:

    @abstractmethod
    def signin(self, request) -> EtherUser:
        raise NotImplementedError

    @abstractmethod
    def login(self, request, username, password, check_pass: bool) -> EtherUser:
        raise NotImplementedError

    @abstractmethod
    def logout(self, request):
        raise NotImplementedError

    @abstractmethod
    def is_logged_in(self, request, user_address) -> bool:
        raise NotImplementedError

    @abstractmethod
    def get_user_address_by_name(self, request, username) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_user_contracts_by_name(self, request, username) -> tuple:
        raise NotImplementedError

    @abstractmethod
    def set_contract_address_to_user(self, username, contract_address) -> bool:
        raise NotImplementedError


class UserRepositoryImpl(UserRepository):

    def signin(self, user: EtherUser) -> EtherUser:
        try:
            user.save()
            return user
        except Exception as exc:
            logger.error(exc)
            return None

    def login(self, request, username, password, address, check_pass: bool) -> EtherUser:

        if check_pass:
            # TODO add password validation
            old_user = user_utils.get_user_by_active_address(address)
            if old_user:
                old_user[0].save(active_eth_address=None)
            user = authenticate(request=request, username=username, password=password)
            if user is not None:
                user.active_eth_address = address
                # user.date_modified = datetime.datetime.now()
                try:
                    user.save(update_fields=['active_eth_address'])
                    return user
                except Exception as exc:
                    logger.error(exc)
                logger.info("Login succeed. User address " + str(user.active_eth_address) + " for user " + username)
                return user
            else:
                return None
        else:
            old_user = user_utils.get_user_by_active_address(address)
            if old_user:
                old_user[0].save(active_eth_address=None)
            user = authenticate(request=request, username=username, password=password)
            if user is not None:
                user.active_eth_address = address
                try:
                    user.save(update_fields=['active_eth_address'])
                    logger.info("Login succeed. User address " + str(user.active_eth_address) + " for user " + username)
                    return user
                except Exception as exc:
                    logger.error(exc)
            else:
                return None

    def logout(self, username) -> str:
        user = EtherUser.objects.get(username=username)
        address = user.active_eth_address
        if user is not None:
            user.active_eth_address = None
            try:
                user.save(update_fields=['active_eth_address'])
                return address
            except Exception as exc:
                logger.error(exc)
                return False

    def is_logged_in(self, request, user_address) -> bool:
        try:
            user_addresses = EtherUser.objects.filter(active_eth_address=user_address)

            if user_addresses.count() > 0:
                return True
            else:
                return False
        except Exception as exc:
            logger.exception(exc)
            return False

    def get_user_address_by_name(self, request, username) -> str:
        try:
            user = EtherUser.objects.get(username=username)
            if user is not None:
                address = user.active_eth_address
                return address
            else:
                logger.warning("User " + username + " does not exist.")
                return None
        except Exception as exc:
            logger.warning("User " + username + " does not exist. " + str(exc))
            return None

    def get_user_contracts_by_name(self, request, username):
        try:
            user = EtherUser.objects.get(username=username)
            if user is not None:
                addresses = user.contract_addresses
                return addresses
            else:
                logger.warning("User " + username + " does not exist.")
                return None
        except Exception as exc:
            logger.warning("User " + username + " does not exist. " + str(exc))
            return None

    def set_contract_address_to_user(self, username=None, active_eth_address=None, contract_address=None) -> bool:
        if username:
            user = user_utils.get_user_by_name(username)
        else:
            user = user_utils.get_user_by_active_address(active_eth_address)
        user.contract_addresses.append(contract_address)
        try:
            user.save(update_fields=['contract_addresses'])
            logger.info("Contract address " + contract_address + "was added to user " + username + " successfully")
            return True
        except Exception as exc:
            logger.error(exc)
            return False


repository = UserRepositoryImpl()
