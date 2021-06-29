from datetime import datetime
from enum import Enum

from playhouse.flask_utils import FlaskDB

from peewee import (
    CharField,
    ForeignKeyField,
    DateTimeField,
    DecimalField,
    IntegerField,
)

db = FlaskDB()


class BaseStrEnum(str, Enum):

    @property
    def choices(cls):
        return [(member.value, member.label) for member in cls]


class StatusEnum(BaseStrEnum):
    PAID = 'Paid'
    DONE = 'Done'


class EntryTypeEnum(BaseStrEnum):
    RESTAURANT = 'Restaurant'
    TAKEAWAY = 'Takeaway'
    TAKEAWAY_SIMPLE = 'Takeaway Simple'
    DELIVERY = 'Delivery'


class Customer(db.Model):
    first_name = CharField()
    last_name = CharField()


class Company(db.Model):
    name = CharField(unique=True)


class CustomerCompany(db.Model):
    customer = ForeignKeyField(Customer)
    company = ForeignKeyField(Company)


class Floor(db.Model):
    name = CharField(unique=True)
    company = ForeignKeyField(Company)


class Table(db.Model):
    name = CharField(default='')
    floor = ForeignKeyField(Floor)


class Entry(db.Model):
    status = CharField(
        choices=StatusEnum.choices, default=StatusEnum.PAID.value)
    entry_type = CharField(
        choices=EntryTypeEnum.choices, default=EntryTypeEnum.RESTAURANT.value)
    net_total = DecimalField(max_digits=10, decimal_places=2)
    gross_total = DecimalField(max_digits=10, decimal_places=2)
    tip = DecimalField(max_digits=10, decimal_places=2, default=0)
    user_id = IntegerField()
    customer = ForeignKeyField(Customer)
    company = ForeignKeyField(Company)
    table = ForeignKeyField(Table, null=True)
    created = DateTimeField(default=datetime.utcnow)
    modified = DateTimeField()
    finalized = DateTimeField()
    print_date = DateTimeField(null=True)

    def save(self, *args, **kwargs):
        self.modified = datetime.utcnow()
        super().save(*args, **kwargs)
