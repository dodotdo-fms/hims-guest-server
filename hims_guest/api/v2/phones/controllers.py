# -*- coding: utf-8 -*-

from hims_guest import db, Log
from flask import Blueprint, request, jsonify
from flask_restful import Resource, Api, reqparse, abort, marshal
from werkzeug.datastructures import FileStorage
from werkzeug.exceptions import HTTPException
from sqlalchemy import exc
from hims_guest.models.db_models import Phone
from hims_guest.models.rest_fields import phone_fields, phone_list_fields
from hims_guest.common.timeutil import str_to_time

api_phone = Blueprint('phone', __name__, url_prefix='/api/v2/phones')
phone_rest = Api(api_phone)

class PhoneItemList(Resource):

    def __init__(self):
        self.phone_post_parser = reqparse.RequestParser()
        self.phone_post_parser.add_argument(
            'uuid',
            location='json',
            type=str,
            help='uuid of the phone',
        )
        self.phone_post_parser.add_argument(
            'name',
            location='json',
            type=str,
            help='Phone name',
        )
        self.phone_post_parser.add_argument(
            'room_number',
            location='json',
            type=str,
            help='Room number that the phone is located',
        )

    def post(self):
        try:
            args = self.phone_post_parser.parse_args()
            phone = Phone.query.filter_by(uuid=args.uuid).first()
            if phone is not None:
                if args.name is not None:
                    phone.name = args.name
                if args.room_number is not None:
                    phone.room_number = args.room_number
            else:
                if args.name is None or args.room_number is None:
                    abort(404, message='Wrong request, name and room_number is required')
                phone = Phone(uuid=args.uuid, name=args.name, room_number=args.room_number)
                db.session.add(phone)
            db.session.commit()

            return marshal(phone, phone_fields, envelope='results')

        except HTTPException as e:
            Log.error(e.message)
            raise
        except exc.SQLAlchemyError as e:
            Log.error(e.message)
            db.session.rollback()
            return abort(503, message='SQLAlchemy error : '+str(e.message))

        except Exception as e:
            print e.message
            Log.error({'message':e.message})
            return abort(500, message='Unexpected error : '+str(e.message))

    def get(self):
        try:
            floor = request.args.get('floor')
            phone_query = []
            if floor is not None:
                phone_query.append(Phone.floor == floor)
            phone_list = Phone.query.filter(*phone_query).all()
            return marshal({'results': phone_list}, phone_list_fields)

        except HTTPException as e:
            Log.error(e.message)
            raise
        except exc.SQLAlchemyError as e:
            Log.error(e.message)
            db.session.rollback()
            return abort(503, message='SQLAlchemy error : '+str(e.message))

        except Exception as e:
            Log.error({'message':e.message})
            return abort(500, message='Unexpected error : '+str(e.message))



class PhoneItem(Resource):

    def __init__(self):
        self.phone_post_parser = reqparse.RequestParser()
        self.phone_post_parser.add_argument(
            'name',
            location='json',
            type=str,
            help='Phone name',
        )
        self.phone_post_parser.add_argument(
            'room_number',
            location='json',
            type=str,
            help='Room number that the phone is located',
        )
        self.phone_post_parser.add_argument(
            'gcm_register_id',
            location='json',
            type=str,
            help='GCM register id for downstream push'
        )
        self.phone_post_parser.add_argument(
            'clean_date_time',
            location='json',
            type=str,
            help='Clean date time'
        )

    def put(self, phone_id):
        try:
            args = self.phone_post_parser.parse_args()
            phone = Phone.query.filter_by(id=phone_id).first()
            if phone is None:
                abort(404, message='Phone id {} not exists'.format(phone_id))
            else:
                if args.name is not None:
                    phone.name = args.name
                if args.room_number is not None:
                    phone.room_number = args.room_number
                if args.gcm_register_id is not None:
                    phone.gcm_register_id = args.gcm_register_id
                if args.clean_date_time is not None:
                    clean_date_time = str_to_time(args.clean_date_time)
                    if clean_date_time is None:
                        abort(406, message='wrong format on clean_date_time, are you sure to formatting %H:%M?')
                    else:
                        phone.clean_date_time = clean_date_time
                db.session.add(phone)
                db.session.commit()
                return marshal(phone, phone_fields, envelope='results')

        except HTTPException as e:
            Log.error(e.message)
            raise
        except exc.SQLAlchemyError as e:
            Log.error(e.message)
            db.session.rollback()
            return abort(503, message='SQLAlchemy error : '+str(e.message))
        except Exception as e:
            Log.error({'message':e.message})
            return abort(500, message='Unexpected error : '+str(e.message))

    def delete(self, phone_id):
        try:
            phone = Phone.query.filter_by(id=phone_id).first()
            if phone is None:
                abort(404, message='Phone id {} not exists'.format(phone_id))
            else:
                db.session.delete(phone)
                db.session.commit()
                return jsonify({'results': 'success'})

        except HTTPException as e:
            Log.error(e.message)
            raise
        except exc.SQLAlchemyError as e:
            Log.error(e.message)
            db.session.rollback()
            return abort(503, message='SQLAlchemy error : '+str(e.message))

        except Exception as e:
            Log.error({'message':e.message})
            return abort(500, message='Unexpected error : '+str(e.message))

    def get(self, phone_id):
        try:
            phone = Phone.query.filter_by(id=phone_id).first()
            if phone is None:
                abort(404, message='Phone id {} not exists'.format(phone_id))
            else:
                return marshal(phone, phone_fields, envelope='results')

        except HTTPException as e:
            Log.error(e.message)
            raise
        except exc.SQLAlchemyError as e:
            Log.error(e.message)
            db.session.rollback()
            return abort(503, message='SQLAlchemy error : '+str(e.message))

        except Exception as e:
            Log.error({'message':e.message})
            return abort(500, message='Unexpected error : '+str(e.message))



class PhoneDataItem(Resource):
    def delete(self, phone_id):
        try:
            phone = Phone.query.filter_by(id=phone_id).first()
            if phone is None:
                abort(404, message='Phone id {} not exists'.format(phone_id))
            else:
                # TODO : GCM to phone

                return jsonify({'results': 'success'})

        except HTTPException as e:
            Log.error(e.message)
            raise
        except exc.SQLAlchemyError as e:
            Log.error(e.message)
            db.session.rollback()
            return abort(503, message='SQLAlchemy error : '+str(e.message))

        except Exception as e:
            Log.error({'message':e.message})
            return abort(500, message='Unexpected error : '+str(e.message))


phone_rest.add_resource(PhoneItemList, '')
phone_rest.add_resource(PhoneItem, '/<phone_id>')
phone_rest.add_resource(PhoneDataItem, '/<phone_id>/data')