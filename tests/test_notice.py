# -*- coding: utf-8 -*-

import json
import unittest
import tempfile
import os
from pprint import pprint
from hims_guest.models.db_models import Phone, Notice
from hims_guest import app, db


class NoticeTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        app.config['TESTING'] = True
        try:
            db.init_app(app)
        except AssertionError as e:
            print e.message

    def setUp(self):
        self.app = app.test_client()
        db.create_all()
        # Employee
        notice_list = [
            {
                'content': '1',
            },
            {
                'content': '2',
            },
            {
                'content': '3',
            },
        ]

        # create dummy phone
        for each_notice in notice_list:
            notice = Notice(
                content = each_notice['content']
            )
            db.session.add(notice)
        db.session.commit()

    def test_notice_get(self):

        # Get notice list
        rv = self.app.get('/api/v2/notices',
                          headers={'Content-Type': 'application/json'})
        self.assertEqual(rv.status_code, 200)
        res_json = json.loads(rv.data)
        self.assertEqual(len(res_json['results']), 3)

    def test_notice_api(self):
        # Post notice
        rv = self.app.post('/api/v2/notices',
                          data=json.dumps({
                              'content': '201'
                          }),
                          headers={'Content-Type': 'application/json'})
        self.assertEqual(rv.status_code, 200)
        res_json = json.loads(rv.data)
        notice_id = res_json['results']['id']

        # Update posted notice
        content = 'hi'
        rv = self.app.put('/api/v2/notices/'+str(notice_id),
                          data=json.dumps({
                              'content': content
                          }),
                          headers={'Content-Type': 'application/json'})
        self.assertEqual(rv.status_code, 200)
        res_json = json.loads(rv.data)
        self.assertEqual(notice_id, res_json['results']['id'])
        self.assertEqual(content, res_json['results']['content'])

        # Delete posted phone
        rv = self.app.delete('/api/v2/notices/'+str(notice_id),
                          headers={'Content-Type': 'application/json'})
        self.assertEqual(rv.status_code, 200)
        res_json = json.loads(rv.data)



    def test_wrong_notice(self):
        # No name
        rv = self.app.post('/api/v2/notices',
                          data=json.dumps({
                              'uuid': '5',
                              'room_number': '201'
                          }),
                          headers={'Content-Type': 'application/json'})
        self.assertEqual(rv.status_code, 406)


        rv = self.app.get('/api/v2/notices/11',
                          headers={'Content-Type': 'application/json'})
        self.assertEqual(rv.status_code, 404)
        pprint(json.loads(rv.data))


    def tearDown(self):
        db.drop_all()
