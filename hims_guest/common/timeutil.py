# -*- coding: utf-8 -*-

import ast
from datetime import datetime
from dateutil import tz
from email.utils import formatdate
from calendar import timegm

def datetime_to_rfc822(dt):
    """
    See :func:`email.utils.formatdate` for more info on the RFC 822 format.

    :param dt: datetime
    :return: rfc822 formatted timestamp
    """
    if dt is None:
        return None
    return formatdate(timegm(dt.utctimetuple()))

def dump_datetime(value):
    if value is None:
        return None
    return value.strftime("%m/%d/%Y %H:%M")

def dump_date(value):
    if value is None:
        return None
    return value.strftime("%m/%d/%Y")
def dump_time(value):
    if value is None:
        return None
    return value.strftime("%H:%M")


def str_to_date(date_str):
    """ dump string of today's date to date object"""
    try:
        return datetime.strptime(date_str, "%m/%d/%Y").date()
    except:
        return None


def str_to_time(time_str):
    """ dump string of today's time to time object"""
    try:
        return datetime.strptime(time_str, "%H:%M").time()
    except:
        return None