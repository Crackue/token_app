from __future__ import unicode_literals
import datetime
from mongoengine import *
from mongoengine.base import fields


class ContractModel(Document):
    contract_name = StringField(max_length=100)
    contract_address = StringField(max_length=100)
    contract_owner = StringField(max_length=100)
    token_name = StringField(max_length=100)
    token_symbol = StringField(max_length=100)
    token_supply = IntField()
    token_functions = ListField(StringField(max_length=150, min_length=1))
    txid = StringField(
        max_length=150,
        unique=True,
        help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.',
        required=True
    )
    gas_price = StringField(max_length=100)
    gas_limit = StringField(max_length=100)
    gas_used = StringField(max_length=100)
    confirmations = IntField()
    block_number = IntField()
    timestamp_transaction = IntField()
    logs = ListField(fields.ComplexBaseField())
    date_modified = DateTimeField(default=datetime.datetime.now())
