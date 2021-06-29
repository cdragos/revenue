from datetime import datetime, timedelta
from decimal import Decimal

from freezegun import freeze_time

from app.models import Company, Customer, Entry


@freeze_time("2018-01-10 01:00:01")
def test_get_hourly(client):
    company = Company.create(name='Nory')
    customer = Customer.create(first_name='John', last_name='Doe')
    user_id = 1

    now = datetime.now()
    entries = [{
        'company': company,
        'customer': customer,
        'net_total': Decimal(95.55),
        'gross_total': Decimal(108.45),
        'created': now,
        'user_id': user_id,
    }, {
        'company': company,
        'customer': customer,
        'net_total': Decimal(60.08),
        'gross_total': Decimal(68.9),
        'created': now,
        'user_id': user_id,
    }, {
        'company': company,
        'customer': customer,
        'net_total': Decimal(49.82),
        'gross_total': Decimal(59.05),
        'created': now + timedelta(hours=1),
        'user_id': user_id,
    }, {
        'company': company,
        'customer': customer,
        'net_total': Decimal(30.51),
        'gross_total': Decimal(35.5),
        'created': now + timedelta(hours=1),
        'user_id': user_id,
    }, {
        'company': company,
        'customer': customer,
        'net_total': Decimal(97.12),
        'gross_total': Decimal(113.5),
        'created': now + timedelta(days=1),
        'user_id': user_id,
    }]
    Entry.insert_many(entries).execute()

    resp = client.get(
        f'/api/hourly?start_date=2018-01-10&company_id={company.id}')
    assert resp.status_code == 200
    assert resp.json == {
        'results': {
            '00:00:00': '0.00',
            '01:00:00': '177.35',
            '02:00:00': '94.55',
            '03:00:00': '0.00',
            '04:00:00': '0.00',
            '05:00:00': '0.00',
            '06:00:00': '0.00',
            '07:00:00': '0.00',
            '08:00:00': '0.00',
            '09:00:00': '0.00',
            '10:00:00': '0.00',
            '11:00:00': '0.00',
            '12:00:00': '0.00',
            '13:00:00': '0.00',
            '14:00:00': '0.00',
            '15:00:00': '0.00',
            '16:00:00': '0.00',
            '17:00:00': '0.00',
            '18:00:00': '0.00',
            '19:00:00': '0.00',
            '20:00:00': '0.00',
            '21:00:00': '0.00',
            '22:00:00': '0.00',
            '23:00:00': '0.00'
        }
    }
