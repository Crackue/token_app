from mongoengine import *
import datetime
from django.contrib.auth import validators

username_validator = validators.UnicodeUsernameValidator()


class EtherUser(Document):
    username = StringField(
        max_length=150,
        unique=True,
        help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.',
        validation=username_validator,
        required=True
    )
    first_name = StringField(max_length=100)
    last_name = StringField(max_length=100)
    email = EmailField()
    eth_addresses = ListField(StringField(max_length=150, min_length=10))
    active_eth_address = StringField(max_length=150, min_length=10)
    date_modified = DateTimeField(default=datetime.datetime.now())
    contract_addresses = ListField(StringField(max_length=150, min_length=10))
