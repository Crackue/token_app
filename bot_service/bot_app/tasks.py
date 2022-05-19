import logging
from celery import shared_task
from bot_app import views

logger = logging.getLogger('celery')


@shared_task(name="process_telegram_event", ignore_result=True)
def process_telegram_event(update_json):
    return views.process_telegram_event(update_json)


@shared_task(name="error_handler")
def error_handler(request, exc, traceback):
    logger.error(f"Task {request.id} raised exception: {exc}", exc_info=traceback)
