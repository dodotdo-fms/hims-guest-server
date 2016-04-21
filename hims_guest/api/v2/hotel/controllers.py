# -*- coding: utf-8 -*-

from hims_guest import db, Log
from flask import Blueprint, request, current_app, session, jsonify
from flask_restful import Resource, Api, reqparse, abort, marshal
from werkzeug.datastructures import FileStorage
from werkzeug.exceptions import HTTPException
from sqlalchemy import exc

api_hotel = Blueprint('hotel', __name__, url_prefix='/api/v2/hotels')
auth_rest = Api(api_hotel)

class Hotel(Resource):

    def __init__(self):
        self.hotel_post_parser = reqparse.RequestParser()
        self.hotel_post_parser.add_argument(
            'phone_number',
            location='json', required=True,
            type=str,
            help='phone number of the hotel',
        )
        self.hotel_post_parser.add_argument(
            'website_url',
            location='json',
            type=str,
            help='Website URL of the hotel',
        )
        self.hotel_post_parser.add_argument(
            'content',
            location='json',
            type=str,
            help='Hotel information content',
        )

    def post(self):
        try:
            if 'application/json' in request.headers['Content-Type']:
                args = self.auth_post_parser.parse_args()

            elif 'application/x-www-form-urlencoded' in request.headers['Content-Type']:
                main_img = request.form['main_img']
            else:
                return abort(406, message='server cannot understand')


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







