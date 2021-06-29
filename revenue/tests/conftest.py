import pytest
from peewee import SqliteDatabase

from app import create_app
from app.models import (
    Company,
    Customer,
    CustomerCompany,
    Entry,
    Floor,
    Table,
)

MODELS = (
    Company,
    Customer,
    CustomerCompany,
    Entry,
    Floor,
    Table,
)


@pytest.fixture
def client():
    test_db = SqliteDatabase(":memory:")
    test_db.bind(MODELS, bind_refs=False, bind_backrefs=False)
    test_db.connect()
    test_db.create_tables(MODELS)

    app = create_app(config={"DATABASE": "sqlite:///:memory:"})
    with app.test_client() as client:
        yield client

    test_db.drop_tables(MODELS)
    test_db.close()
