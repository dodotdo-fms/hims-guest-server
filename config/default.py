# -*- coding: utf-8 -*-

import os

class Config(object):
    APP_NAME = 'hims_guest'
    ROOT_DIR = os.path.dirname(os.getcwd())


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/hims_guest.db'
    DEBUG = False
    LOG_LEVEL = 'info'
    MOD = 'PRO'

class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/hims_guest.db'
    DEBUG = True
    LOG_LEVEL = 'debug'
    MOD = 'DEV'
    