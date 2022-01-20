from __future__ import unicode_literals

import brownie

from django.db import models
from mongoengine import *
from mongoengine.base import fields


class Transaction(Document):
    contract_name = StringField(max_length=100)
    fn_name = StringField(max_length=100)
    txid = StringField(
        max_length=150,
        unique=True,
        help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.',
        required=True
    )
    sender = StringField(max_length=100)
    receiver = StringField(max_length=100)
    value = IntField()
    gas_price = StringField(max_length=100)
    gas_limit = StringField(max_length=100)
    gas_used = StringField(max_length=100)
    input = StringField(max_length=200)
    confirmations = IntField()
    nonce = StringField(max_length=200)
    block_number = IntField()
    timestamp = IntField()
    txindex = StringField(max_length=100)
    contract_address = StringField(max_length=100)
    logs = ListField(fields.ComplexBaseField())
    status = EnumField(brownie.network.transaction.Status)
