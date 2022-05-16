import logging
from celery import shared_task
from contracts.services.repository import repository

logger = logging.getLogger('celery')


@shared_task(name="deploy", ignore_result=True)
def deploy(address_owner, token_name, token_symbol, token_supply_val, key_wallet):
    tx_event = repository.deploy(address_owner, token_name, token_symbol, token_supply_val, key_wallet)
    logger.info(f"tx_event: {tx_event}")
    return tx_event


@shared_task(name="contract_by_address", time_limit=10)
def contract_by_address(contract_address):
    return repository.contract_by_address(contract_address)


@shared_task(name="load_contract", time_limit=60)
def load_contract(contract_address, address_owner):
    return repository.load_contract(contract_address, address_owner)


@shared_task(name="error_handler")
def error_handler(request, exc, traceback):
    logger.error(f"Task {request.id} raised exception: {exc}", exc_info=traceback)
