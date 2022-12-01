import json
import os
import logging
import threading
from time import sleep

from django.http import HttpResponse, JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from bot_app.handlers.auth_handlers import auth_handlers as auth_handler
from bot_app.handlers.erc20_handlers import (balance_of_handlers, transfer_handler,
                                             approve_handler, allowance_handler,
                                             transfer_from_handler, base_handlers, get_info_handler)
from bot_app.handlers.main_menu_handlers import (on_start_menu_handler, my_contract_handler,
                                                 on_create_contract_handler, on_interact_with_contract_handler)
from bot_app.handlers.create_contract_handlers import erc20_handler
from bot_service.settings import env
from utils import bot_request_utils as request_utils, handlers_utils as utils, session_utils
from telegram import Bot, Update
from telegram.ext import (Updater, CommandHandler, Dispatcher)
from bot_app.models import TelegramMessage
from bot_app import tasks

logger = logging.getLogger(__name__)
DEBUG = env('DEBUG')
BOT_TOKEN = os.getenv('BOT_TOKEN')
TELEGRAM_URL = os.getenv('TELEGRAM_URL')
WEB_HOOK_URL = os.getenv('WEB_HOOK_URL')

n_workers = 1 if DEBUG else 4
bot = Bot(token=BOT_TOKEN)
_updater_ = Updater(token=BOT_TOKEN, workers=n_workers)


def setup_dispatcher(dp):
    dp.add_handler(CommandHandler("start", on_start_menu_handler.command_start))
    # dp.add_handler(auth_handler.signin_conv_handler)
    dp.add_handler(auth_handler.login_conv_handler)
    dp.add_handler(CommandHandler("logout", auth_handler.logout))
    dp.add_handler(CommandHandler("my_contracts", my_contract_handler.get_contracts_command))
    dp.add_handler(CommandHandler("create_contract", on_create_contract_handler.command_create_contract))
    dp.add_handler(erc20_handler.erc20_conv_handler)
    dp.add_handler(CommandHandler("main_menu", on_start_menu_handler.command_start))
    dp.add_handler(on_interact_with_contract_handler.interact_with_contract_handler)
    dp.add_handler(CommandHandler("name", base_handlers.get_contract_name))
    dp.add_handler(CommandHandler("symbol", base_handlers.get_contract_symbol))
    dp.add_handler(CommandHandler("decimals", base_handlers.get_contract_decimals))
    dp.add_handler(CommandHandler("total_supply", base_handlers.get_contract_total_supply))
    dp.add_handler(CommandHandler("balance", balance_of_handlers.balance_of))
    dp.add_handler(transfer_handler.transfer_conv_handler)
    dp.add_handler(approve_handler.approve_conv_handler)
    dp.add_handler(allowance_handler.allowance_conv_handler)
    dp.add_handler(transfer_from_handler.transfer_from_conv_handler)
    dp.add_handler(CommandHandler("contract_info", get_info_handler.get_contract_info))
    return dp


def run_pooling(dispatcher: Dispatcher):
    setup_dispatcher(dispatcher)

    # it is really useful to send '👋' emoji to developer
    # when you run local test
    # bot.send_message(text='👋', chat_id=<YOUR TELEGRAM ID>)
    dispatcher.bot.delete_webhook()
    dispatcher.bot.set_webhook(f"{TELEGRAM_URL}{BOT_TOKEN}/setWebhook?url={WEB_HOOK_URL}/bot/webhook_post/")
    bot_info = dispatcher.bot.get_me()
    bot_link = f"https://t.me/" + bot_info["username"]
    logger.info(dispatcher.bot.getWebhookInfo())
    logger.info(f"Pooling of '{bot_link}' started")


@csrf_exempt
def start_bot(request) -> HttpResponse:
    logger.info("START_BOT_REQUEST")
    run_pooling(_updater_.dispatcher)
    return HttpResponse("START_BOT_RESPONSE")


class TelegramBotWebhookView(View):
    def post(self, request, *args, **kwargs):

        if not bool(DEBUG):
            update_from_queue = tasks.update_handler(json.loads(request.body))
            process_telegram_event(update_from_queue)
        else:
            update_from_queue = tasks.update_handler.s(json.loads(request.body))\
                .on_error(tasks.error_handler.s())\
                .apply_async()
            process_telegram_event(update_from_queue.get())

        return JsonResponse({"ok": "POST request processed"})

    def get(self, request, *args, **kwargs):  # for debug
        return JsonResponse({"ok": "Get request received! But nothing done"})


def process_telegram_event(update_json):
    update = Update.de_json(update_json, _updater_.bot)
    if request_utils.is_bot(update):
        return

    ss = session_utils.get_session_store(update)

    if ss.has_key(str(update['update_id'])):
        logger.warning("Message " + str(update['update_id']) + " is not processed")
        return
    else:
        ss.__setitem__(str(update['update_id']), str(update['update_id']))
        ss.save()
        logger.info(f"update_id: {ss.get(str(update['update_id']))}")
    _updater_.dispatcher.process_update(update)


def save_message(update):
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


if bool(DEBUG):
    run_pooling(_updater_.dispatcher)
