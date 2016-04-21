from flask_restful import Resource, Api, fields, reqparse, abort, marshal_with
from hims_guest.common.timeutil import dump_time

class TimeItem(fields.Raw):
    def format(self, value):
        try:
            return dump_time(value)
        except:
            return None

phone_fields = {
    'id': fields.Integer,
    'uuid': fields.String,
    'name': fields.String,
    'room_number': fields.String,
    'floor': fields.String,
    'recent_notice_timestamp': fields.DateTime,
    'register_timestamp': fields.DateTime,
    'clean_date_time': TimeItem(attribute='clean_date_time'),
}

phone_list_fields = {
    'results': fields.List(fields.Nested(phone_fields))
}
