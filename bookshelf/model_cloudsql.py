# Copyright 2015 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import six


builtin_list = list


db = SQLAlchemy()


def init_app(app):
    db.init_app(app)


def from_sql(row):
    """Translates a SQLAlchemy model instance into a dictionary"""
    d = {}
    for column in row.__table__.columns:
        d[column.name] = six.text_type(getattr(row, column.name))

    return d


# [START model]
class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    author = db.Column(db.String(255))
    publishedDate = db.Column(db.String(255))
    imageUrl = db.Column(db.String(255))
    description = db.Column(db.String(255))
    createdBy = db.Column(db.String(255))
    createdById = db.Column(db.String(255))

    def __repr__(self):
        return "<Book(title='%s', author=%s)" % (self.title, self.author)
# [END model]


class Box(db.Model):
    __tablename__ = 'Boxes'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(1023))
    name = db.Column(db.String(255))
    major = db.Column(db.String(255))
    seeking = db.Column(db.Text(16383))
    offering = db.Column(db.Text(16383))
    email = db.Column(db.String(255))
    type = db.Column(db.Integer)
    category = db.Column(db.Integer)
    category2 = db.Column(db.Integer)
    category3 = db.Column(db.Integer)
    createdBy = db.Column(db.String(255))
    createdById = db.Column(db.String(255))

    def __repr__(self):
        return "<Box(title='%s', author=%s)" % (self.title, self.name)


def list(limit=500, cursor=None):
    cursor = int(cursor) if cursor else 0
    query = (Box.query
             .order_by(Box.title)
             .limit(limit)
             .offset(cursor))
    books = builtin_list(map(from_sql, query.all()))
    next_page = cursor + limit if len(books) == limit else None
    return (books, next_page)


def list_by_user(user_id, limit=100, cursor=None):
    cursor = int(cursor) if cursor else 0
    query = (Box.query
             .filter_by(createdById=user_id)
             .order_by(Box.title)
             .limit(limit)
             .offset(cursor))
    books = builtin_list(map(from_sql, query.all()))
    next_page = cursor + limit if len(books) == limit else None
    return (books, next_page)


def read(id):
    result = Box.query.get(id)
    if not result:
        return None
    return from_sql(result)


def create(data):
    book = Box(**data)
    db.session.add(book)
    db.session.commit()
    return from_sql(book)


# [START update]
def update(data, id):
    book = Box.query.get(id)
    for k, v in data.items():
        setattr(book, k, v)
    db.session.commit()
    return from_sql(book)
# [END update]


def delete(id):
    Box.query.filter_by(id=id).delete()
    db.session.commit()


def _create_database():
    """
    If this script is run directly, create all the tables necessary to run the
    application.
    """
    app = Flask(__name__)
    app.config.from_pyfile('../config.py')
    init_app(app)
    with app.app_context():
        db.create_all()
    print("All tables created")


if __name__ == '__main__':
    _create_database()
