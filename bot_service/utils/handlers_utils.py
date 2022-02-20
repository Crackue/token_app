import logging
import datetime
from telegram import Update
from bot_app.models import TelegramMessage

logger = logging.getLogger(__name__)


def convert_update_to_telegram_message(update: Update) -> TelegramMessage:
    update_id = update['update_id']
    message = TelegramMessage()
    message.message = update.message.to_dict()
    message.update_id = update_id
    return message


def convert_contract_json_to_str_reply(contract_json):
    date_num_sec = contract_json['date_modified']['$date'] / 1000
    # TODO set timezone from bot
    date_creation = datetime.datetime.fromtimestamp(date_num_sec).strftime(
        '%Y-%m-%d %H:%M:%S')
    contracts = 'Contract Name: ' + contract_json['contract_name'] + '\n' + \
                'Contract Address: ' + contract_json['contract_address'] + '\n' + \
                'Contract Owner: ' + contract_json['contract_owner'] + '\n' + \
                'Token Name: ' + contract_json['token_name'] + '\n' + \
                'Token Symbol: ' + contract_json['token_symbol'] + '\n' + \
                'Token Supply: ' + str(contract_json['token_supply']) + '\n' + \
                'Token Functions: ' + str(contract_json['token_functions']) + '\n' + \
                'Date Creation: ' + str(date_creation)
    return contracts
