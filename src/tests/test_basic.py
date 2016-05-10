import unittest
import datetime
import json

from microservice import create_app
from pymongo import read_preferences
from flask import current_app


class BasicsTestCase(unittest.TestCase):
    def setUp(self):
        config = {
            'db': 'test_testproject',
            'host': '127.0.0.1',
            'port': 27017,
            'read_preference': read_preferences.ReadPreference.PRIMARY,
        }
        self.app = create_app(config)
        self.app.config['TESTING'] = True
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.testapp = self.app.test_client()
        from microservice.api.models import Record
        r1 = Record(
            uid='1',
            name='John Doe',
            date=datetime.datetime.strptime(
                '2015-05-12T14:36:00.451765',
                "%Y-%m-%dT%H:%M:%S.%f"
            ),
            md5checksum='5662edb6868e98505e0f4344d2abd47b'
        )
        r2 = Record(
            uid='2',
            name='Jane Doe',
            date=datetime.datetime.strptime(
                '2015-05-13T14:36:00.451765',
                "%Y-%m-%dT%H:%M:%S.%f"
            ),
            md5checksum='0cf6399e2739304b73b41162735679fb'
        )
        r1.save()
        r2.save()

    def tearDown(self):
        from microservice.api.models import Record
        Record.objects.delete()
        self.app_context.pop()

    def test_app_exists(self):
        self.assertFalse(current_app is None)

    def test_app_is_testing(self):
        self.assertTrue(current_app.config['TESTING'])

    def test_add_correct_record(self):
        r = {
            'uid': '1',
            'name': 'John Doe',
            'date': '2015-05-14T14:36:00.451765',
            'md5checksum': 'e8c83e232b64ce94fdd0e4539ad0d44f',
        }
        return self.testapp.post('/api/', data=r, follow_redirects=True)

    def test_add_incorrect_record_wronguid(self):
        r = {
            'uid': '2',
            'name': 'John Doe',
            'date': '2015-05-12T12:36:00.451765',
            'md5checksum': '410ae0c69c9fcd521e5877be676348b5',
        }
        resp = self.testapp.post('/api/',
                                 data=json.dumps(r),
                                 content_type='application/json',
                                 follow_redirects=True)
        assert "Error. name - uid missmatch" in resp.data

    def test_add_incorrect_record_wrongname(self):
        r = {
            'uid': '1',
            'name': 'John ',
            'date': '2015-05-12T14:36:00.451765',
            'md5checksum': 'b0fc89e4b7ea0b2276ad17fb9994b1fe',
        }
        resp = self.testapp.post('/api/',
                                 data=json.dumps(r),
                                 content_type='application/json',
                                 follow_redirects=True)
        assert "Error. name - uid missmatch" in resp.data

    def test_add_incorrect_record_wrongmd5(self):
        r = {
            'uid': '1',
            'name': 'John Doe',
            'date': '2015-05-12T14:36:00.451765',
            'md5checksum': 'e8c83e232b64ce94f',
        }
        resp = self.testapp.post('/api/',
                                 data=json.dumps(r),
                                 content_type='application/json',
                                 follow_redirects=True)
        assert "Error. Checksum doesn't match" in resp.data

    def test_add_incorrect_record_notjson(self):
        r = 'John Doe'
        resp = self.testapp.post('/api/',
                                 data=r,
                                 content_type='application/json',
                                 follow_redirects=True)
        self.assertEqual(resp.status_code, 400)

    def test_add_incorrect_record_datetime(self):
        r = {
            'uid': '1',
            'name': 'John Doe',
            'date': '2015-05-14T14:36',
            'md5checksum': 'e8c83e232b64ce94fdd0e4539ad0d44f',
        }
        resp = self.testapp.post('/api/',
                                 data=json.dumps(r),
                                 content_type='application/json',
                                 follow_redirects=True)
        assert 'Error. Invalid date format' in resp.data

    def test_add_incorrect_record_missingfield(self):
        r = {
            'uid': '1',
            'name': 'John Doe',
            'md5checksum': 'e8c83e232b64ce94fdd0e4539ad0d44f',
        }
        resp = self.testapp.post('/api/',
                                 data=json.dumps(r),
                                 content_type='application/json',
                                 follow_redirects=True)
        assert 'Error. date field is missing' in resp.data

    def test_get_record(self):
        resp = self.testapp.get('/api/1/2015-05-12/', follow_redirects=True)
        data = json.loads(resp.data)
        self.assertEqual(len(data.keys()), 1)
