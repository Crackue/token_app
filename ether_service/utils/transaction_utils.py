import logging

from brownie.network.transaction import TransactionReceipt
from ether_network.models import Transaction
from brownie.convert import datatypes

logger = logging.getLogger(__name__)


def transaction_receipt_handler(tx: TransactionReceipt) -> Transaction:
    transaction_model = Transaction()
    transaction_model.contract_name = tx.contract_name
    transaction_model.fn_name = tx.fn_name
    transaction_model.txid = tx.txid
    transaction_model.sender = str(tx.sender)
    transaction_model.receiver = tx.receiver
    # TODO what 'value' is???
    transaction_model.value = int(tx.value.to('ether'))
    transaction_model.gas_price = str(tx.gas_price)
    transaction_model.gas_limit = str(tx.gas_limit)
    transaction_model.gas_used = str(tx.gas_used)
    transaction_model.input = tx.input
    transaction_model.confirmations = tx.confirmations
    transaction_model.nonce = str(tx.nonce)
    transaction_model.block_number = int(tx.block_number)
    transaction_model.timestamp = tx.timestamp
    transaction_model.txindex = str(tx.txindex)
    transaction_model.contract_address = tx.contract_address
    transaction_model.logs = tx.logs
    transaction_model.status = tx.status
    logger.info(str(tx.logs))
    return transaction_model
