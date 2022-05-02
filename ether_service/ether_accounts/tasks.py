import logging
from celery import shared_task
from ether_accounts.services.accounts_repository import repository

logger = logging.getLogger('celery')


@shared_task(name="add", time_limit=10)
def add(key: str):
    return repository.add(key)


@shared_task(name="remove")
def remove(user_address):
    return repository.remove(user_address)


@shared_task(name="clear")
def clear() -> bool:
    return repository.clear()


@shared_task(name="is_local_account")
def is_local_account(request) -> bool:
    return repository.is_local_account(request)


@shared_task(name="error_handler")
def error_handler(request, exc, traceback):
    logger.error(f"Task {request.id} raised exception: {exc}", exc_info=traceback)
