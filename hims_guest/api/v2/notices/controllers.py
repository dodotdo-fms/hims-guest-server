# -*- coding: utf-8 -*-

from hims_guest import db, Log
from flask import Blueprint, request, jsonify
from flask_restful import Resource, Api, reqparse, abort, marshal
from werkzeug.datastructures import FileStorage
from werkzeug.exceptions import HTTPException
from sqlalchemy import exc, func
from hims_guest.models.db_models import Phone, Notice
from hims_guest.models.rest_fields import notice_fields, notice_list_fields
from hims_guest.common.timeutil import str_to_time, str_to_date

api_notice = Blueprint('notice', __name__, url_prefix='/api/v2/notices')
notice_rest = Api(api_notice)

class NoticeItemList(Resource):

    def __init__(self):
        self.notice_post_parser = reqparse.RequestParser()
        self.notice_post_parser.add_argument(
            'content',
            location='json',
            type=str,
            help='content of notice',
        )

    def post(self):
        try:
            args = self.notice_post_parser.parse_args()

            if args.content is None:
                abort(406, message='Content of the notice is empty. Fill the content')
            notice = Notice(content=args.content)
            db.session.add(notice)
            db.session.commit()

            # Send to users.
            # TODO, WS or GCM
            return marshal(notice, notice_fields, envelope='results')

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
            query_date = str_to_date(request.args.get('date'))
            notice_query = []
            if query_date is not None:
                notice_query.append(func.DATE(Notice.register_timestamp) == query_date)
            notice_list = Notice.query.filter(*notice_query).all()
            return marshal({'results': notice_list}, notice_list_fields)

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



class NoticeItem(Resource):

    def __init__(self):
        self.notice_post_parser = reqparse.RequestParser()
        self.notice_post_parser.add_argument(
            'content',
            location='json',
            type=str,
            help='content of notice',
        )

    def put(self, notice_id):
        try:
            args = self.notice_post_parser.parse_args()
            notice = Notice.query.filter_by(id=notice_id).first()
            if notice is None:
                abort(404, message='Notice id {} not exists'.format(notice_id))
            else:
                notice.content = args.content
                db.session.commit()
                return marshal(notice, notice_fields, envelope='results')

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

    def delete(self, notice_id):
        try:
            notice = Notice.query.filter_by(id=notice_id).first()
            if notice is None:
                abort(404, message='Notice id {} not exists'.format(notice_id))
            else:
                db.session.delete(notice)
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

    def get(self, notice_id):
        try:
            notice = Notice.query.filter_by(id=notice_id).first()
            if notice is None:
                abort(404, message='Notice id {} not exists'.format(notice_id))
            else:
                return marshal(notice, notice_fields, envelope='results')

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


notice_rest.add_resource(NoticeItemList, '')
notice_rest.add_resource(NoticeItem, '/<notice_id>')
