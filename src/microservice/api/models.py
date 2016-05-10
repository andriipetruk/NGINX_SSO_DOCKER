import datetime
import hashlib
import json
from microservice import db
from collections import OrderedDict


class Record(db.Document):
    uid = db.IntField(required=True)
    name = db.StringField(max_length=255, required=True)
    date = db.DateTimeField(default=datetime.datetime.now, required=True)
    md5checksum = db.StringField(max_length=50, required=True)

    def check_md5(self):
        jstring = json.dumps(OrderedDict([
            ('uid', self.uid),
            ('name', self.name),
            ('date', self.date.strftime("%Y-%m-%dT%H:%M:%S.%f"))
        ]))
        md5 = hashlib.md5(jstring).hexdigest()
        print "Correct md5 checksum for string {js} is {md5}".format(
            md5=md5,
            js=jstring)
        return md5 == self.md5checksum.lower()
