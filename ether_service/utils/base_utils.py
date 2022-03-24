import logging
import sys

logger = logging.getLogger(__name__)


def get_num_with_decimals(amount, decimals) -> int:
    value = int(amount)
    return value * pow(10, decimals)


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
    return None
