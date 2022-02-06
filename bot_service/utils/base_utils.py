import logging
import sys
import requests
from bot_service.settings import USER_SERVICE_HOST, USER_PORT, SCHEME
from urllib.parse import urlunsplit

logger = logging.getLogger(__name__)

USER_NETLOC = USER_SERVICE_HOST + ":" + USER_PORT if SCHEME == "http" else USER_SERVICE_HOST

user_service_base = "user/"
user_service_is_logged_in = "is_logged_in/"
user_service_get_by_name = "get_user_by_name/"
path_is_logged_in = user_service_base + user_service_is_logged_in
path_get_by_name = user_service_base + user_service_get_by_name
user_service_is_logged_in_endpoint = urlunsplit((SCHEME, USER_NETLOC, path_is_logged_in, "", ""))
user_service_get_by_name_endpoint = urlunsplit((SCHEME, USER_NETLOC, path_get_by_name, "", ""))


def get_num_with_decimals(amount, decimals) -> int:
    return amount * pow(10, decimals)


def num_without_decimals(amount, decimals) -> int:
    return amount / pow(10, decimals)


def amount_validate(value) -> str:
    try:
        _value_ = int(value)
    except Exception as exc:
        logger.error(exc)
        return "Amount should be number"

    if _value_ < 0:
        return "Should not be less then 0"
    elif _value_ > sys.maxsize:
        return "Amount is too much"
    return _value_


def is_logged_in(username) -> tuple:
    obj = {"username": username}
    try:
        user_address = requests.post(user_service_get_by_name_endpoint, data=obj)
        if user_address.text is None:
            return False, "User does not exist. Probably, you should to sign in"

        obj_address = {"user_address": user_address}

        response = requests.post(user_service_is_logged_in_endpoint, data=obj_address)
        _is_logged_in_ = response.text == 'True'
        if not _is_logged_in_:
            return False, "You should be logged in for this stuff"
    except Exception as exc:
        logger.exception(exc)
        return False, "Something wrong: " + str(exc.args)
    return True, user_address.text


def get_user_address_by_name(username) -> tuple:
    obj = {"username": username}
    try:
        user_address = requests.post(user_service_get_by_name_endpoint, data=obj)
        if user_address.text is None:
            return False, "User " + username + "does not exist"
        return True, user_address.text
    except Exception as exc:
        logger.exception(exc)
        return False, "Something wrong: " + str(exc.args)
