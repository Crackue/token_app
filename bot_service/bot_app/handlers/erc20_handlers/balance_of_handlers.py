import json
import logging
import requests

from utils import base_utils, session_utils
from telegram import Update
from telegram.ext import CallbackContext
from constants import url_constants

logger = logging.getLogger(__name__)


def balance_of(update: Update, context: CallbackContext):
    username = update.message.from_user['username']
    is_logged_in = base_utils.is_logged_in(username)
    if not is_logged_in[0]:
        update.message.reply_text(is_logged_in[1])
        return
    obj = {"address_owner": is_logged_in[1]}
    ss = session_utils.get_session_store(update)
    try:
        session_id = ss['ether_service_session_id']
        cookies = dict(sessionid=session_id)
        response = requests.post(url_constants.ether_erc20_balance_of_endpoint, data=obj, cookies=cookies)
    except KeyError:
        response = requests.post(url_constants.ether_erc20_balance_of_endpoint, data=obj)
        session_id = response.cookies.get_dict()['sessionid']
        ss['ether_service_session_id'] = session_id
        ss.save()

    if not response.status_code == 200:
        update.message.reply_text("FAILED! " + response.reason)
        return

    resp = json.loads(response.text)
    if resp:
        update.message.reply_text("Your balance: " + str(resp))
        logger.info("Balance of user " + username + ": " + str(resp))
    else:
        logger.warning("Get balance_of for user " + username + " is FAILED!: " + str(resp))
        update.message.reply_text("FAILED! " + str(resp))
