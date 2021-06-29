from datetime import datetime, time
from flask import (
    Blueprint,
    jsonify,
    request,
)
from playhouse.flask_utils import get_object_or_404
from peewee import fn

from .exceptions import ValidationException
from .models import Entry, Company, db


api = Blueprint('api', __name__, url_prefix='/api')


@api.route('/hourly')
def hourly():
    start_date = request.args.get('start_date')
    if not start_date:
        raise ValidationException('Start date is required.')

    try:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
    except (ValueError, TypeError):
        raise ValidationException('Start date is not a valid date.')

    company_id = request.args.get('company_id')
    company = get_object_or_404(Company, Company.id == company_id)

    hours = {
        time(i).strftime('%H:%M:%S'): '{:0.2f}'.format(0) for i in range(24)}

    entries = Entry.select(
        db.database.extract_date('hour', Entry.created).alias('hour'),
        fn.SUM(Entry.gross_total).alias('total')
    ).group_by(
        fn.date_trunc('hour', Entry.created)
    ).where(
        Entry.company == company,
        fn.date_trunc('day', Entry.created) == start_date
    ).dicts()[:]

    for entry in entries:
        hours[time(entry['hour']).strftime('%H:%M:%S')] = (
            '{:0.2f}'.format(entry['total']))

    return jsonify({'results': hours})


@api.route('/daily')
def daily():
    # TODO
    return jsonify(msg="implement me")
