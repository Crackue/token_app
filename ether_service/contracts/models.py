from __future__ import unicode_literals
import datetime
from typing import List, Optional

from mongoengine import *
from mongoengine.base import fields
from redis_om import JsonModel, Field


class ContractModel(Document):
    contract_name = StringField(max_length=100)
    contract_address = StringField(max_length=100, unique=True, required=True)
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


class ContractCache(JsonModel):
    contract_name: str
    contract_address: str = Field(index=True)
    contract_owner: str = Field(index=True)
    token_name: str = Field(index=True)
    token_symbol: str
    token_supply: int
    token_functions: List[str] = []
    date_modified: Optional[datetime.datetime] = None

    def __init__(self, contract: ContractModel):
        self.contract_name = contract.contract_name
        self.contract_address = contract.contract_address
        self.contract_owner = contract.contract_owner
        self.token_name = contract.token_name
        self.token_symbol = contract.token_symbol
        self.token_supply = contract.token_supply
        self.token_functions = contract.token_functions
        self.date_modified = contract.date_modified
