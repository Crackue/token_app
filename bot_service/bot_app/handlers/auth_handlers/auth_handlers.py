import logging
import requests
from telegram import Update
from telegram.ext import (CallbackContext, CommandHandler, MessageHandler, ConversationHandler, Filters)
from bot_service.settings import USER_SERVICE_HOST
from urllib.parse import urlunsplit

logger = logging.getLogger(__name__)
# _user_service_ = serviceBot
_user_service_ = 0

KEY, WALLET_ADDRESS = range(2)

SCHEME = "http"
PORT = "8000"
NETLOC = USER_SERVICE_HOST + ":" + PORT

user_service_base = "user/"
user_service_login = "login/"
user_service_logout = "logout/"
user_service_signin = "signin/"

path_login = user_service_base + user_service_login
path_logout = user_service_base + user_service_logout
path_signin = user_service_base + user_service_signin

user_service_login_endpoint = urlunsplit((SCHEME, NETLOC, path_login, "", ""))
user_service_logout_endpoint = urlunsplit((SCHEME, NETLOC, path_logout, "", ""))
user_service_signin_endpoint = urlunsplit((SCHEME, NETLOC, path_signin, "", ""))


def repeat_or_stop(update: Update, context: CallbackContext):
    _text_ = update.message['text']
    if _text_ == 'stop':
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
    key = update.message.text
    obj = {"key": key, "username": username}
    response = None
    try:
        response = requests.post(user_service_login_endpoint, data=obj)
    except Exception as exc:
        logger.exception(exc)

    if response is None:
        logger.info("Request post to " + user_service_login_endpoint + " FAILED")
        update.message.reply_text("Something wrong. Try again later")
        return ConversationHandler.END

    if response.status_code == 200:
        logger.info("User " + str(username) + " logged in successfully")
        update.message.reply_text("Yep! You logged in!")
    else:
        # TODO add more info from response to log
        logger.info("User " + str(username) + " not exist")
        update.message.reply_text("User " + str(username) + " not exist. You should signin")
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
        response = requests.post(user_service_logout_endpoint, data=obj)
    except Exception as exc:
        logger.exception(exc)

    if response is None:
        logger.info("Request post to " + user_service_logout_endpoint + " FAILED")
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
        response = requests.post(user_service_logout_endpoint, data=obj)
    except Exception as exc:
        logger.exception(exc)

    if response is None:
        logger.info("Request post to " + user_service_login_endpoint + " FAILED")
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
