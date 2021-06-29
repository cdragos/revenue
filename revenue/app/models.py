from datetime import datetime
from enum import Enum

from playhouse.flask_utils import FlaskDB

from pewee import (
    CharField,
    ForeignKey,
    DatetimeField,
    DecimalField,
    IntegerField,
)

db = FlaskDB()


class StatusEnum(str, Enum):
    PAID = 'Paid'
    DONE = 'Done'


class EntryTypeEnum(str, Enum):
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
    customer = ForeignKey(Customer)
    company = ForeignKey(Company)


class Floor(db.Model):
    name = CharField(unique=True)
    company = ForeignKey(Company)


class Table(db.Model):
    name = CharField(default='')
    floor = ForeignKey(Floor)


class Entry(db.Model):
    status = CharField(choices=StatusEnum.choices)
    entry_type = CharField(choices=EntryTypeEnum.choices)
    net_total = DecimalField(max_digits=10, decimal_places=2)
    gross_total = DecimalField(max_digits=10, decimal_places=2)
    tip = DecimalField(max_digits=10, decimal_places=2, default=0)
    user_id = IntegerField()
    customer = ForeignKey(Customer)
    company = ForeignKey(Company)
    table = ForeignKey(Table)
    created = DatetimeField(default=datetime.utcnow)
    modified = DatetimeField()
    finalized = DatetimeField()
    print_date = DatetimeField(null=True)

    def save(self, *args, **kwargs):
        self.modified = datetime.utcnow()
        super().save(*args, **kwargs)
