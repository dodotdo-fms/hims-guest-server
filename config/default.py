# -*- coding: utf-8 -*-

import os

class Config(object):
    APP_NAME = 'hims_guest'
    ROOT_DIR = os.path.dirname(os.getcwd())

    ALLOWED_EXTENSIONS = ['jpg', 'jpeg', 'png']
    FILE_CONTENT_TYPES = { # these will be used to set the content type of S3 object. It is binary by default.
        'jpg': 'image/jpeg',
        'jpeg': 'image/jpeg',
        'png': 'image/png'
    }
    ROOM_FLOOR_QUOTIENT = 100  # floor = room / ROOM_FLOOR_QUOTIENT

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/hims_guest.db'
    DEBUG = False
    LOG_LEVEL = 'info'
    MOD = 'PRO'
    BASE_SERVER = 'http://localhost:8080'
    API_SERVER = BASE_SERVER + '/api/'
    FILE_SERVER = BASE_SERVER + '/file/'

class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/hims_guest.db'
    DEBUG = True
    LOG_LEVEL = 'debug'
    MOD = 'DEV'
    BASE_SERVER = 'http://localhost:8080'
    API_SERVER = BASE_SERVER + '/api/'
    FILE_SERVER = BASE_SERVER + '/file/'

