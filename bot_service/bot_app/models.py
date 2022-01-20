from django.db import models
from mongoengine import *
from mongoengine.base import fields
import datetime


class TelegramMessage(Document):
    message = fields.ComplexBaseField()
    update_id = IntField()
    date_modified = DateTimeField(default=datetime.datetime.now())

