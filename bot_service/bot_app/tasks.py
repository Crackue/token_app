import logging
from celery import shared_task

logger = logging.getLogger('celery')


@shared_task(name="error_handler")
def error_handler(request, exc, traceback):
    logger.error(f"Task {request.id} raised exception: {exc}", exc_info=traceback)


@shared_task(name="update_handler")
def update_handler(update):
    return update
