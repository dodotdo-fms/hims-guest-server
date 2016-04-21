# -*- coding: utf-8 -*-

import json
import unittest
import tempfile
import os
from pprint import pprint
from hims_guest.models.db_models import Phone
from hims_guest import app, db


class PhoneTestCase(unittest.TestCase):

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
        phone_list = [
            {
                'uuid': '1',
                'name': 'phone1',
                'room_number': '101',
                'floor': '1'
            },
            {
                'uuid': '2',
                'name': 'phone2',
                'room_number': '102',
                'floor': '1'
            },
            {
                'uuid': '3',
                'name': 'phone3',
                'room_number': '208',
                'floor': '2'
            }
        ]

        # create dummy phone
        for each_phone in phone_list:
            if Phone.query.filter_by(uuid=each_phone['uuid']).first() is not None:
                print 'exists'
                continue
            phone = Phone(
                    uuid = each_phone['uuid'],
                    name = each_phone['name'],
                    room_number = each_phone['room_number'],
                    floor = each_phone['floor']
            )
            db.session.add(phone)
        db.session.commit()

    def test_phone_get(self):

        # Get phone list
        rv = self.app.get('/api/v2/phones',
                          headers={'Content-Type': 'application/json'})
        self.assertEqual(rv.status_code, 200)
        res_json = json.loads(rv.data)
        self.assertEqual(len(res_json['results']), 3)


        # Get phone list on floor args
        rv = self.app.get('/api/v2/phones?floor=1',
                          headers={'Content-Type': 'application/json'})
        self.assertEqual(rv.status_code, 200)
        res_json = json.loads(rv.data)
        self.assertEqual(len(res_json['results']), 2)




    def test_phone_api(self):
        # Post phone
        rv = self.app.post('/api/v2/phones',
                          data=json.dumps({
                              'uuid': '5',
                              'name': 'phone5',
                              'room_number': '201'
                          }),
                          headers={'Content-Type': 'application/json'})
        self.assertEqual(rv.status_code, 200)
        res_json = json.loads(rv.data)
        phone_id = res_json['results']['id']

        # Get Posted phone
        rv = self.app.get('/api/v2/phones/'+str(phone_id),
                          data=json.dumps({
                              'uuid': '5',
                              'name': 'phone5',
                              'room_number': '201'
                          }),
                          headers={'Content-Type': 'application/json'})
        self.assertEqual(rv.status_code, 200)
        res_json = json.loads(rv.data)
        self.assertEqual(phone_id, res_json['results']['id'])



        # Update posted phone
        name = 'phone523'
        rv = self.app.put('/api/v2/phones/'+str(phone_id),
                          data=json.dumps({
                              'name': name,
                              'room_number': '202',
                              'gcm_register_id': '12',
                              'clean_date_time': '20:42'
                          }),
                          headers={'Content-Type': 'application/json'})
        self.assertEqual(rv.status_code, 200)
        res_json = json.loads(rv.data)
        self.assertEqual(phone_id, res_json['results']['id'])
        self.assertEqual(name, res_json['results']['name'])

        # Delete posted phone
        rv = self.app.delete('/api/v2/phones/1',
                          headers={'Content-Type': 'application/json'})
        self.assertEqual(rv.status_code, 200)
        res_json = json.loads(rv.data)




    def test_phone_data_clean(self):
        # clean  phone data
        rv = self.app.delete('/api/v2/phones/1/data',
                          headers={'Content-Type': 'application/json'})
        self.assertEqual(rv.status_code, 200)
        res_json = json.loads(rv.data)

    def test_wrong_phone_post(self):
        # No name
        rv = self.app.post('/api/v2/phones',
                          data=json.dumps({
                              'uuid': '5',
                              'room_number': '201'
                          }),
                          headers={'Content-Type': 'application/json'})
        self.assertEqual(rv.status_code, 404)

        # No room_number
        rv = self.app.post('/api/v2/phones',
                          data=json.dumps({
                              'uuid': '5',
                              'name': 'phone5b'
                          }),
                          headers={'Content-Type': 'application/json'})
        self.assertEqual(rv.status_code, 404)

        # Duplicated phone name
        rv = self.app.post('/api/v2/phones',
                          data=json.dumps({
                              'uuid': '6',
                              'name': 'phone1',
                              'room_number': '202'
                          }),
                          headers={'Content-Type': 'application/json'})
        self.assertEqual(rv.status_code, 503)


        rv = self.app.get('/api/v2/phones/1',
                          headers={'Content-Type': 'application/json'})
        self.assertEqual(rv.status_code, 200)
        pprint(json.loads(rv.data))


    def test_wrong_phone_get(self):
        # Wrong phone id
        rv = self.app.get('/api/v2/phones/9',
                          headers={'Content-Type': 'application/json'})
        self.assertEqual(rv.status_code, 404)






    def tearDown(self):
        db.drop_all()
