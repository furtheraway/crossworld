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

from bookshelf import get_model, oauth2
from flask import Blueprint, current_app, redirect, render_template, request, \
    session, url_for
from datetime import datetime

crud = Blueprint('crud', __name__)


# [START list]
@crud.route("/")
def list():
    token = request.args.get('page_token', None)
    books, next_page_token = get_model().list(cursor=token)
    news1 = get_model().read_news(id=3)

    return render_template(
        "list.html",
        books=books,
        next_page_token=next_page_token,
        news1=news1)
# [END list]


@crud.route("/my_post")
@oauth2.required
def list_mine():
    token = request.args.get('page_token', None)

    books, next_page_token = get_model().list_by_user(
        user_id=session['profile']['id'],
        cursor=token)

    return render_template(
        "list_mine.html",
        books=books,
        next_page_token=datetime.utcnow(),
        user_id=session['profile']['emails'][0]['value'])
        # above for testing purpose, in my post header;

@crud.route("/category/<cid>")
def list_category(cid):
    token = request.args.get('page_token', None)

    books, next_page_token = get_model().list_by_category(
        cid=cid,
        cursor=token)

    return render_template(
        "list_category.html",
        books=books,
        next_page_token=next_page_token,
        cid=cid)

# Add a logout handler.
@crud.route('/logout')
def logout():
    # Delete the user's profile and the credentials stored by oauth2.
    del session['profile']
    oauth2.storage.delete()
    return redirect('/')
    # return redirect(request.referrer or '/')


@crud.route('/<id>')
def view(id):
    book = get_model().read(id)
    return render_template("view.html", book=book)


# [START add]
@crud.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        data = request.form.to_dict(flat=True)

        # If the user is logged in, associate their profile with the new book.
        if 'profile' in session:
            data['createdBy'] = session['profile']['displayName']
            data['createdById'] = session['profile']['id']
            data['email_true'] = session['profile']['emails'][0]['value']
            data['create_T'] = datetime.utcnow()
            data['modify_T'] = datetime.utcnow()

        book = get_model().create(data)

        return redirect(url_for('.view', id=book['id']))

    return render_template("form.html", action="Add", book={})
# [END add]


@crud.route('/<id>/edit', methods=['GET', 'POST'])
def edit(id):
    book = get_model().read(id)
    if not ('profile' in session and (book['createdById'] == session['profile']['id'] or session['profile']['id']=="111854835568927675810")):
        return render_template("nope.html")

    if request.method == 'POST':
        data = request.form.to_dict(flat=True)
        
        # If the user is logged in, associate their profile with the new book.
        if 'profile' in session:
            data['createdBy'] = session['profile']['displayName']
            data['createdById'] = session['profile']['id']
            data['email_true'] = session['profile']['emails'][0]['value']
            data['modify_T'] = datetime.utcnow()

        book = get_model().update(data, id)

        return redirect(url_for('.view', id=book['id']))

    return render_template("form.html", action="Edit", book=book)


@crud.route('/<id>/delete')
def delete(id):
    book = get_model().read(id)
    if ('profile' in session and (book['createdById'] == session['profile']['id'] or session['profile']['id']=="111854835568927675810")):
        get_model().delete(id)
        return redirect(request.referrer or '/')
    else:
        return render_template("nope.html")


@crud.route('/job')
def list_all():
    if ('profile' in session and session['profile']['id']=="111854835568927675810"):
        token = request.args.get('page_token', None)
        books, next_page_token = get_model().list_all(
            cursor=token)
        return render_template(
            "list_mine.html",
            books=books,
            next_page_token=next_page_token)
    else:
        return render_template("nope.html")



