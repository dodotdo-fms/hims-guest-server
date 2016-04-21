# -*- coding: utf-8 -*-

import logging
from logging import handlers
import os
from pythonjsonlogger import jsonlogger

class Log:

    __log_level_map = {
        'debug' : logging.DEBUG,
        'info' : logging.INFO,
        'warn' : logging.WARN,
        'error' : logging.ERROR,
        'critical' : logging.CRITICAL
        }

    __hims_logger = None

    @staticmethod
    def init(logger_name='hims-logger',
             log_level='debug',
             log_filepath='hims-guest_server/log/hims.log'):
        Log.__hims_logger = logging.getLogger(logger_name)
        Log.__hims_logger.setLevel(Log.__log_level_map.get(log_level, 'warn'))
        formatter = jsonlogger.JsonFormatter('%(asctime) %(levelname) %(module) %(funcName) %(lineno) %(message)')

        # logstashLogHandler = logstash.LogstashHandler(logger_name, 5959, version=1)
        if log_level == 'debug' or 'error':
            streamLogHandler = logging.StreamHandler()
            streamLogHandler.setFormatter(formatter)
            Log.__hims_logger.addHandler(streamLogHandler)

        fileLogHandler = logging.handlers.TimedRotatingFileHandler(
                os.path.join(log_filepath, 'hims_guest.log'), when='D', interval=1)
        fileLogHandler.setFormatter(formatter)
        # Log.__hims_logger.addHandler(logstashLogHandler)
        Log.__hims_logger.addHandler(fileLogHandler)



    @staticmethod
    def debug(msg):
        Log.__hims_logger.debug(msg)

    @staticmethod
    def info(msg):
        Log.__hims_logger.info(msg)

    @staticmethod
    def warn(msg):
        Log.__hims_logger.warn(msg)

    @staticmethod
    def error(msg):
        Log.__hims_logger.error(msg)

    @staticmethod
    def critical(msg):
        Log.__hims_logger.critical(msg)
