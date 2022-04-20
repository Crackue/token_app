import logging
from celery import shared_task
from utils import contract_utils, base_utils
from erc20.services.repository import repository

logger = logging.getLogger('celery')


@shared_task(name="name")
def name(contract_address):
    contract = contract_utils.get_contract(contract_address)
    return repository.name(contract)


@shared_task(name="symbol")
def symbol(contract_address):
    contract = contract_utils.get_contract(contract_address)
    return repository.symbol(contract)


@shared_task(name="decimals")
def decimals(contract_address):
    contract = contract_utils.get_contract(contract_address)
    return repository.decimals(contract)


@shared_task(name="total_supply")
def total_supply(contract_address):
    contract = contract_utils.get_contract(contract_address)
    return repository.total_supply(contract)


@shared_task(name="balance_of")
def balance_of(address_owner, contract_address):
    contract = contract_utils.get_contract(contract_address)
    return repository.balance_of(address_owner, contract)


@shared_task(name="transfer", ignore_result=True)
def transfer(contract_address, address_to, value, address_owner):
    contract = contract_utils.get_contract(contract_address)
    tx_event = repository.transfer(address_owner, address_to, value, contract)
    logger.info(f"tx_event: {tx_event}")
    return tx_event


@shared_task(name="transfer_from", ignore_result=True)
def transfer_from(contract_address, address_owner, address_from, address_to, val):
    contract = contract_utils.get_contract(contract_address)
    tx_event = repository.transfer_from(address_owner, address_from, address_to, val, contract)
    logger.info(f"tx_event: {tx_event}")
    return tx_event


@shared_task(name="approve", ignore_result=True)
def approve(contract_address, address_spender, val, address_owner):
    contract = contract_utils.get_contract(contract_address)
    tx_event = repository.approve(address_owner, address_spender, val, contract)
    logger.info(f"tx_event: {tx_event}")
    return tx_event


@shared_task(name="allowance")
def allowance(contract_address, address_owner, address_spender):
    contract = contract_utils.get_contract(contract_address)
    _allowance_ = repository.allowance(address_owner, address_spender, contract)
    value = base_utils.num_without_decimals(_allowance_, 18)
    return value


@shared_task(name="base_contract_info")
def base_contract_info(contract_address):
    contract = contract_utils.get_contract(contract_address)
    return repository.base_contract_info(contract)


@shared_task(name="error_handler")
def error_handler(request, exc, traceback):
    logger.error(f"Task {request.id} raised exception: {exc}", exc_info=traceback)
