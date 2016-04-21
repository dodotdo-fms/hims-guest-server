# -*- coding: utf-8 -*-

import os
import eventlet
from flask import Flask
from flask_socketio import SocketIO
from database import db

app = Flask(__name__)
app.config.from_object('config.default.DevelopementConfig')

# logging module
from hims_logger import Log
log_filepath = os.path.join(app.config['ROOT_DIR'], 'log')
Log.init(log_filepath=log_filepath, log_level=app.config['LOG_LEVEL'])
Log.info("START HIMS SERVER")


# SOCKET
async_mode = 'eventlet'
eventlet.monkey_patch()
socketio = SocketIO(app, async_mode=async_mode, binary=True, ping_timeout=15, engineio_logger=True)

# init
socketio.init_app(app)
db.init_app(app)

from .api.v2.hotel.controllers import api_hotel
# from .api.v2.items.controllers import api_item
# from .api.v2.mails.controllers import api_mail
# from .api.v2.notices.controllers import api_notice
# from .api.v2.phones.controllers import api_phone
# from .web.v2.views import web_view
#
app.register_blueprint(api_hotel)
# app.register_blueprint(api_item)
# app.register_blueprint(api_mail)
# app.register_blueprint(api_notice)
# app.register_blueprint(api_phone)
# app.register_blueprint(web_view)
#
