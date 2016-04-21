# -*- coding: utf-8 -*-
from flask.ext.sqlalchemy import SQLAlchemy

# declarative part is not used right now
# because there is clear benefit to using flask-sqlalchemy over sqlalchemy
# TODO But, it seems that flask-sqlalchemy is not maintained. Needs to be considered
# reference : flask-docs-kr.readthedocs.org/ko/latest/patterns/sqlalchemy.html

# Instantiate and start DB
db = SQLAlchemy()