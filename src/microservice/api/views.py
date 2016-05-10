import datetime

from flask import jsonify, request
from microservice.api.models import Record
from . import api


@api.route('/<int:uid>/<date>/', methods=['GET'])
def get_record(uid, date):
    minDate = datetime.datetime.strptime(date, "%Y-%m-%d")
    maxDate = minDate + datetime.timedelta(days=1)
    records = Record.objects(uid=uid, date__gte=minDate, date__lt=maxDate)
    return jsonify({'response': records})


@api.route('/', methods=['POST'])
def put_record():
    if not request.json:
        return jsonify({'response': 'Error. request should be a JSON string'})
    data = request.json
    VALID_FIELDS = ['uid', 'name', 'date', 'md5checksum']
    for field in VALID_FIELDS:
        if field not in data:
            return jsonify({
                'response': 'Error. {0} field is missing'.format(field)
            })
    try:
        date = datetime.datetime.strptime(data.get('date'),
                                          "%Y-%m-%dT%H:%M:%S.%f")
    except ValueError:
        return jsonify({
                'response': 'Error. Invalid date format. Date should be given'
                ' in a %%Y-%%m-%%dT%%H:%%M:%%S.%%f format'
            })
    r = Record(
        uid=data.get('uid'),
        name=data.get('name'),
        date=date,
        md5checksum=data.get('md5checksum')
    )
    if not r.check_md5():
        return jsonify({'response': "Error. Checksum doesn't match"})
    uidRecord = Record.objects(uid=r.uid).first()
    nameRecord = Record.objects(name=r.name).first()
    if uidRecord and r.name != uidRecord.name:
        return jsonify({'response': "Error. name - uid missmatch"})
    if nameRecord and r.uid != nameRecord.uid:
        return jsonify({'response': "Error. name - uid missmatch"})
    r.save()
    return jsonify({'response': 'record successfuly added'})
