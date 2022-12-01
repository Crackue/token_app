
import logging
import json
import requests

from telegram import Update
from telegram.ext import (CallbackContext, CommandHandler, MessageHandler, ConversationHandler, Filters)
from constants import url_constants
from utils import base_utils, session_utils

logger = logging.getLogger(__name__)

KEY, WALLET_ADDRESS = range(2)


def repeat_or_stop(update: Update, context: CallbackContext):
    _text_ = update.message['text']
    if str(_text_).lower() == 'stop':
        update.message.reply_text('Buy! See you later...')
        return ConversationHandler.END
    else:
        update.message.reply_text('You should to reply on message. If you want to finished just type \"stop\"')


def login(update: Update, context: CallbackContext):
    logger.info(update.to_json())
    update.message.reply_text("Enter your wallet key:")
    return KEY


def get_key(update: Update, context: CallbackContext):
    username = update.message.from_user['username']
    address_owner = base_utils.get_user_address_by_name(username)
    if not address_owner[0]:
        update.message.reply_text(address_owner[1])
        return ConversationHandler.END

    key = update.message.text
    obj = {"key": key, "username": username, "address_owner": address_owner}

    ss = session_utils.get_session_store(update)
    try:
        session_id = ss['user_service_session_id']
        cookies = dict(sessionid=session_id)
        response = requests.post(url_constants.user_service_login_endpoint, data=obj, cookies=cookies)
    except KeyError:
        response = requests.post(url_constants.user_service_login_endpoint, data=obj)
        session_id = response.cookies.get_dict()['sessionid']
        ss['user_service_session_id'] = session_id
        ss.save()

    if not response.status_code == 200:
        update.message.reply_text("Something goes wrong... " + response.reason + ". Try again")
        return ConversationHandler.END
    resp = json.loads(response.text)

    if resp is None:
        logger.info("Request post to " + url_constants.user_service_login_endpoint + " FAILED")
        update.message.reply_text("Something wrong. Try again later")
        return ConversationHandler.END

    if resp[0]:
        logger.info("User " + str(username) + " logged in successfully")
        update.message.reply_text("Yep! You logged in!")
    else:
        # TODO add more info from response to log
        logger.info("User " + str(username) + " not exist")
        update.message.reply_text("FAILED. " + resp[1])
    return ConversationHandler.END


def cancel(update: Update, context: CallbackContext):
    update.message.reply_text('Just try again...')
    return ConversationHandler.END


login_conv_handler = ConversationHandler(
    entry_points=[CommandHandler('login', login)],
    states={
        KEY: [MessageHandler(Filters.reply, get_key), MessageHandler(Filters.text, repeat_or_stop)],
    },
    fallbacks=[CommandHandler('cancel', cancel)],
)


def logout(update: Update, context: CallbackContext):
    username = update.message.from_user['username']
    obj = {"username": username}
    response = None
    try:
        response = requests.post(url_constants.user_service_logout_endpoint, data=obj)
    except Exception as exc:
        logger.exception(exc)

    if response is None:
        logger.info("Request post to " + url_constants.user_service_logout_endpoint + " FAILED")
        update.message.reply_text("Something wrong. Try again later")
        return ConversationHandler.END

    if response.status_code == 200:
        logger.info("User " + str(username) + " logged out successfully")
        update.message.reply_text("Done! You logged out!")
    else:
        # TODO add more info from response to log
        logger.info("User " + str(username) + " log out FAILED")
        update.message.reply_text("Oops! log out FAILED! :(")


def signin(update: Update, context: CallbackContext):
    logger.info(update.to_json())
    update.message.reply_text("Enter your wallet address:")
    return WALLET_ADDRESS


def get_address(update: Update, context: CallbackContext):
    eth_address = update.message.text
    username = update.message.from_user['username']
    obj = {"eth_address": eth_address, "username": username}
    response = None
    try:
        response = requests.post(url_constants.user_service_signin_endpoint, data=obj)
    except Exception as exc:
        logger.exception(exc)
        return ConversationHandler.END

    if response is None:
        logger.info("Request post to " + url_constants.user_service_signin_endpoint + " FAILED")
        update.message.reply_text("Something wrong. Try again later")
        return ConversationHandler.END

    if response.status_code == 200:
        logger.info("User " + str(username) + " signed in successfully")
        update.message.reply_text("It's Done! :)")
    else:
        # TODO add more info from response to log
        logger.info("User " + str(username) + " sign in FAILED")
        update.message.reply_text("Signin FAILED! Sorry for that :(")
    return ConversationHandler.END


signin_conv_handler = ConversationHandler(
    entry_points=[CommandHandler('signin', signin)],
    states={
        WALLET_ADDRESS: [MessageHandler(Filters.reply, get_address), MessageHandler(Filters.text, repeat_or_stop)],
    },
    fallbacks=[MessageHandler(Filters.regex(r'stop'), cancel)],
)
