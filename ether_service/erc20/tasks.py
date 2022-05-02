import logging
from celery import shared_task
from utils import contract_utils, base_utils
from erc20.services.repository import repository

logger = logging.getLogger('celery')


@shared_task(name="name", time_limit=10)
def name(contract_address):
    contract = contract_utils.get_contract(None, contract_address, contract_utils.LOCAL_DB)
    return repository.name(contract)


@shared_task(name="symbol", time_limit=10)
def symbol(contract_address):
    contract = contract_utils.get_contract(None, contract_address, contract_utils.LOCAL_DB)
    return repository.symbol(contract)


@shared_task(name="decimals", time_limit=10)
def decimals(contract_address):
    contract = contract_utils.get_contract(None, contract_address, contract_utils.LOCAL_DB)
    return repository.decimals(contract)


@shared_task(name="total_supply", time_limit=10)
def total_supply(address_owner, contract_address):
    contract = contract_utils.get_contract(address_owner, contract_address, contract_utils.LOCAL_DB)
    return repository.total_supply(contract)


@shared_task(name="balance_of", time_limit=20)
def balance_of(address_owner, contract_address):
    contract = contract_utils.get_contract(address_owner, contract_address, contract_utils.EXPLORER)
    return repository.balance_of(address_owner, contract)


@shared_task(name="transfer", ignore_result=True)
def transfer(contract_address, address_to, value, address_owner):
    contract = contract_utils.get_contract(address_owner, contract_address, contract_utils.EXPLORER)
    tx_event = repository.transfer(address_owner, address_to, value, contract)
    logger.info(f"tx_event: {tx_event}")
    return tx_event


@shared_task(name="transfer_from", ignore_result=True)
def transfer_from(contract_address, address_owner, address_from, address_to, val):
    contract = contract_utils.get_contract(address_owner, contract_address, contract_utils.EXPLORER)
    tx_event = repository.transfer_from(address_owner, address_from, address_to, val, contract)
    logger.info(f"tx_event: {tx_event}")
    return tx_event


@shared_task(name="approve", ignore_result=True)
def approve(contract_address, address_spender, val, address_owner):
    contract = contract_utils.get_contract(address_owner, contract_address, contract_utils.EXPLORER)
    tx_event = repository.approve(address_owner, address_spender, val, contract)
    logger.info(f"tx_event: {tx_event}")
    return tx_event


@shared_task(name="allowance", time_limit=10)
def allowance(contract_address, address_owner, address_spender):
    contract = contract_utils.get_contract(address_owner, contract_address, contract_utils.EXPLORER)
    _allowance_ = repository.allowance(address_owner, address_spender, contract)
    value = base_utils.num_without_decimals(_allowance_, 18)
    return value


@shared_task(name="base_contract_info", time_limit=10)
def base_contract_info(contract_address):
    contract = contract_utils.get_contract(None, contract_address, contract_utils.LOCAL_DB)
    return repository.base_contract_info(contract)


@shared_task(name="error_handler")
def error_handler(request, exc, traceback):
    logger.error(f"Task {request.id} raised exception: {exc}", exc_info=traceback)
