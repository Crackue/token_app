import json
import os
import sys
import threading
import logging
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from bot_app.handlers.onstart_handler import on_start_handler as start_handler
from bot_app.handlers.auth_handlers import auth_handlers as auth_handler
from bot_app.handlers.erc20_handlers import (base_handlers, transfer_handler,
                                             approve_handler, allowance_handler,
                                             transfer_from_handler)
from utils import bot_request_utils as request_utils, handlers_utils as utils
from telegram import Bot, Update
import telegram.error
from telegram.ext import (Updater, CommandHandler, Dispatcher)

from bot_app.models import TelegramMessage

logger = logging.getLogger(__name__)
DEBUG = bool(os.getenv('DEBUG'))
BOT_TOKEN = os.getenv('BOT_TOKEN')
TELEGRAM_URL = os.getenv('TELEGRAM_URL')
WEB_HOOK_URL = os.getenv('WEB_HOOK_URL')
bot = Bot(BOT_TOKEN)
try:
    TELEGRAM_BOT_USERNAME = bot.get_me()["username"]
except telegram.error.Unauthorized:
    logging.error(f"Invalid TELEGRAM_TOKEN.")
    sys.exit(1)


def setup_dispatcher(dp):
    dp.add_handler(CommandHandler("start", start_handler.command_start))
    dp.add_handler(auth_handler.signin_conv_handler)
    dp.add_handler(auth_handler.login_conv_handler)
    dp.add_handler(CommandHandler("logout", auth_handler.logout))
    dp.add_handler(CommandHandler("balance", base_handlers.balance_of))
    dp.add_handler(transfer_handler.transfer_conv_handler)
    dp.add_handler(approve_handler.approve_conv_handler)
    dp.add_handler(allowance_handler.allowance_conv_handler)
    dp.add_handler(transfer_from_handler.transfer_from_conv_handler)
    # dp.add_handler(MessageHandler(Filters.all, all_message_handler.handle_message))
    return dp


def run_pooling():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    setup_dispatcher(dp)

    # it is really useful to send '👋' emoji to developer
    # when you run local test
    # bot.send_message(text='👋', chat_id=<YOUR TELEGRAM ID>)
    bot.delete_webhook()
    bot.set_webhook(TELEGRAM_URL + BOT_TOKEN + "/setWebhook?url=" + WEB_HOOK_URL + "/bot/webhook_post/")
    # updater.start_polling()
    bot_info = Bot(BOT_TOKEN).get_me()
    bot_link = f"https://t.me/" + bot_info["username"]
    logger.info(bot.getWebhookInfo().to_json())
    logger.info(f"Pooling of '{bot_link}' started")


t = threading.Thread(name='bot', target=run_pooling)
t.setDaemon(True)
t.start()


@csrf_exempt
def start_bot(request) -> HttpResponse:
    logger.info("START_BOT_REQUEST")
    # t.start()
    return HttpResponse("START_BOT_RESPONSE")


class TelegramBotWebhookView(View):
    # WARNING: if fail - Telegram webhook will be delivered again.
    # Can be fixed with async celery task execution
    def post(self, request, *args, **kwargs):
        logger.info(request)
        # TODO add load balancer
        process_telegram_event(json.loads(request.body))

        # if DEBUG:
        #     process_telegram_event(json.loads(request.body))
        # else:
        #     # TODO CELERY
        #     # Process Telegram event in Celery worker (async)
        #     # Don't forget to run it and & Redis (message broker for Celery)!
        #     # Read Procfile for details
        #     # You can run all of these services via docker-compose.yml
        #     process_telegram_event.delay(json.loads(request.body))

        return JsonResponse({"ok": "POST request processed"})

    def get(self, request, *args, **kwargs):  # for debug
        return JsonResponse({"ok": "Get request received! But nothing done"})


def process_telegram_event(update_json):
    update = Update.de_json(update_json, bot)
    if request_utils.is_bot(update):
        return
    message = utils.convert_update_to_telegram_message(update)
    try:
        _message_ = TelegramMessage.objects(update_id=message.update_id)
        if not _message_.count() == 0:
            logger.warning("Message " + str(message.update_id) + " is not processed")
            return
        message.save()
        logger.info("Message saved: " + update.to_json())
    except Exception as exc:
        logger.error(exc)
    dispatcher.process_update(update)


n_workers = 1 if DEBUG else 4
dispatcher = setup_dispatcher(Dispatcher(bot, update_queue=None, workers=n_workers, use_context=True))
