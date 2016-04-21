# -*- coding: utf-8 -*-

import time
from datetime import datetime

from hims_guest.database import db
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
from werkzeug.security import generate_password_hash, \
     check_password_hash

from flask import current_app, session
from hims_guest.common.timeutil import datetime_to_rfc822, dump_time


class Hotel(db.Model):
    __tablename__ = 'hotel'
    id = db.Column(db.Integer, primary_key=True)
    main_img_filename = db.Column(db.String(128))
    phone_number = db.Column(db.String(64))
    website_url = db.Column(db.String(128))
    content = db.Column(db.Text)
    register_timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, **kwargs):
        super(Hotel, self).__init__(**kwargs)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'main_img_filename': self.main_img_filename,
            'phone_number': self.phone_number,
            'website_url': self.website_url,
            'main_img_url': current_app.config['FILE_SERVER']+self.main_img_filename if self.main_img_filename is not None else None,
            'content': self.content,
            'register_timestamp': datetime_to_rfc822(self.register_timestamp)
        }

class Phone(db.Model):
    __tablename__ = 'phone'
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(128), index=True)
    gcm_register_id = db.Column(db.String(128))
    name = db.Column(db.String(64), nullable=False)
    room_number = db.Column(db.String(64))
    floor = db.Column(db.String(32))
    recent_notice_timestamp = db.Column(db.DateTime)
    register_timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    clean_date_time = db.Column(db.Time)

    def __init__(self, **kwargs):
        super(Phone, self).__init__(**kwargs)
        # TODO test whether this is valid statement
        if 'room_number' in kwargs:
            self.floor = str(int(kwargs['room_number']) / current_app.config['ROOM_FLOOR_QUOTIENT'])


    @property
    def serialize(self):
        return {
            'id': self.id,
            'uuid': self.uuid,
            'name': self.name,
            'room_nubmer': self.room_number,
            'recent_notice_timestamp': datetime_to_rfc822(self.recent_notice_timestamp),
            'register_timestamp': datetime_to_rfc822(self.register_timestamp),
            'clean_date_time': dump_time(self.clean_date_time)
        }


class ItemClass(db.Model):
    __tablename__ = 'item_class'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(32), nullable=False)
    title = db.Column(db.String(128), nullable=False)
    subtitle = db.Column(db.String(256))
    main_img_filename = db.Column(db.String(128))
    register_timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    item = db.relationship('Item', backref='item_class', cascade='save-update, delete', lazy="joined")

    def __init__(self, **kwargs):
        super(ItemClass, self).__init__(**kwargs)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'type': self.type,
            'title': self.title,
            'subtitle': self.subtitle,
            'main_img_url': current_app.config['FILE_SERVER']+self.main_img_filename if self.main_img_filename is not None else None,
            'register_timestamp': datetime_to_rfc822(self.register_timestamp),
        }



class Item(db.Model):
    __tablename__ = 'item'
    id = db.Column(db.Integer, primary_key=True)
    item_class_id = db.Column(db.Inteer, db.ForeignKey('item_class.id'), nullable=False, index=True)
    type = db.Column(db.String(32), nullable=False)
    title = db.Column(db.String(128), nullable=False)
    subtitle = db.Column(db.String(256))
    main_img_filename = db.Column(db.String(128))
    card_width = db.Column(db.Integer, default=1)
    card_height = db.Column(db.Integer, default=1)
    content = db.Column(db.Text)
    phone_number = db.Column(db.String(64))
    website_url = db.Column(db.String(128))
    register_timestamp = db.Column(db.DateTime, default=datetime.utcnow)


    def __init__(self, **kwargs):
        super(Item, self).__init__(**kwargs)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'item_class_id': self.item_class_id,
            'type': self.type,
            'title': self.title,
            'subtitle': self.subtitle,
            'main_img_url': current_app.config['FILE_SERVER']+self.main_img_filename if self.main_img_filename is not None else None,
            'card_width': self.card_width,
            'card_height': self.card_height,
            'content': self.content,
            'phone_number': self.phone_number,
            'website_url': self.website_url,
            'register_timestamp': datetime_to_rfc822(self.register_timestamp),
        }


class Notice(db.Model):
    __tablename__ = 'notice'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text),
    register_timestamp = db.Column(db.DateTime, default=datetime.utcnow)


    def __init__(self, **kwargs):
        super(Notice, self).__init__(**kwargs)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'content': self.content,
            'register_timestamp': datetime_to_rfc822(self.register_timestamp),
        }



class NoticePhone(db.Model):
    __tablename__ = 'notice_phone'
    notice_id = db.Column(db.Integer, db.ForeignKey('notice.id'), primary_key=True)
    phone_id = db.Column(db.Integer, db.ForeignKey('phone.id'), primary_key=True)
    register_timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, **kwargs):
        super(Notice, self).__init__(**kwargs)

    @property
    def serialize(self):
        return {
            'notice_id': self.notice_id,
            'phone_id': self.phone_id,
            'register_timestamp': datetime_to_rfc822(self.register_timestamp),
        }







