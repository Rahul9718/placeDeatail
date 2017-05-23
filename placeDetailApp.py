#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, jsonify, request, abort, make_response
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()
import time

app = Flask(__name__)

app.config.update({'DEBUG': True})

users = [{
    'username': 'rahul',
    'password': 'a',
    'bio': 'leranig flask',
    'age': 20,
    'city': 'delhi',
}, {
    'username': 'shivam',
    'password': 'b',
    'bio': 'best codder of navgurukul',
    'age': 33,
    'city': 'mubai',
}]

places = [{
    'placeName': 'taj mahal',
    'added_on': time.strftime('%d/%m/%Y'),
    'detail': 'taj mahal is in agra',
    'username': 'rahul',
    'likes': 10,
    'id': 1,
}, {
    'placeName': 'lal kila',
    'added_on': time.strftime('%d/%m/%Y'),
    'detail': 'this is red in color',
    'username': 'shivam',
    'likes': 15,
    'id': 1,
}, {
    'placeName': 'lotous temple',
    'added_on': time.strftime('%d/%m/%Y'),
    'detail': 'it shape is like lotus',
    'username': 'rahul',
    'likes': 16,
    'id': 2,
}, {
    'placeName': '5 sense',
    'added_on': time.strftime('%d/%m/%Y'),
    'detail': 'this is the love point',
    'username': 'shivam',
    'likes': 14,
    'id': 2,
}]

comments = [{
    'id': 1,
    'username': 'rahul',
    'text': 'this is not a good place to visit',
    'added_on': time.strftime('%d/%m/%Y'),
}, {
    'id': 2,
    'username': 'shivam',
    'text': 'this is not family place',
    'added_on': time.strftime('%d/%m/%Y'),
}]



@auth.get_password
def get_password(username):
    new_user = [user for user in users if username == user['username']]
    if len(new_user) == 0:
        abort(400)
    return new_user[0]['password']


@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'unauthorized access'}), 401)



@app.route('/get/user/user_detail', methods=['GET'])
@auth.login_required
def current_user():
    current_user_detail = [user for user in users if auth.username() == user['username']]
    return jsonify({'user': current_user_detail})



@app.route('/post/user/add_user', methods=['POST'])
@auth.login_required
def signup():
    if not request.json or not 'username' in request.json:
        abort(400)
    add_user = {
        'username': request.json['username'],
        'password': request.json['password'],
        'bio': request.json['bio'],
        'age': request.json['age'],
        'city': request.json['city'],
    }
    users.append(add_user)
    return (jsonify({'users': add_user}), 201)







@app.route('/get/user/user_current_place/<int:place_id>', methods=['GET'])
@auth.login_required
def get_current_place(place_id):
    place = [place for place in places if auth.username() == place['username']]
    one_place = [one_place for one_place in place if place_id == one_place['id']]
    return (jsonify({'place': one_place}), 201)



@app.route('/get/place/currentPlace', methods=['GET'])
@auth.login_required
def current_place():
    place = [place for place in places if auth.username() == place['username']]
    return jsonify({'place': place})



@app.route('/post/place/add_place', methods=['POST'])
@auth.login_required
def add_place():
    if not request.json or not 'placeName' in request.json:
        abort(400)
    add_place = {
        'placeName': request.json['placeName'],
        'added_on': time.strftime('%d/%m/%Y'),
        'detail': request.json['detail'],
        'username': auth.username(),
        'likes': places[-1]['likes'] + 1,
        'id': places[-1]['id'] + 1,
    }
    places.append(add_place)
    return (jsonify({'places': add_place}), 201)



@app.route('/put/user/update_place/<int:place_id>', methods = ['PUT'])
@auth.login_required
def update_place(place_id):
    update_place_value = [update_place_value for update_place_value in places if auth.username() == update_place_value['username'] ]
    place_update = [place_update for place_update in update_place_value if place_id == place_update['id']]
    if len(place_update) == 0:
        abort(400)
    if not request.json:
        abort(400)
    if 'detail' in request.json and type(request.json['detail']) is not unicode:
        abort(400)
    place_update[0]['detail'] = request.json.get('detail', place_update[0]['detail'])
    return jsonify({'update_place': place_update[0]})






@app.route('/get/user/user_comment/<int:comment_id>', methods = ['GET'])
@auth.login_required
def comment_from_id(comment_id):
    user_comment = [user_comment for user_comment in comments if auth.username() ==user_comment['username']]
    one_comment = [one_comment for one_comment in user_comment if comment_id ==one_comment['id']]
    return jsonify({'comment': one_comment}), 201



@app.route('/post/user/add_comment/<int:comment_id>', methods = ['POST'])
@auth.login_required
def add_comment(comment_id):
    if not request.json and not 'text' in request.json:
        abort(400)
    comment = [comment for comment in comments if comment_id == comment['id']]
    current_user_comment =[current_user_comment for current_user_comment in comment if auth.username() == current_user_comment['username']]
    if not request.json:
        abort(400)
    add_more_comment = {
        'text': request.json['text'],
        'username': auth.username(),
        'added_on': time.strftime('%d/%m/%Y')
    }

    comments.append(add_more_comment)
    return jsonify({'comment': current_user_comment})





if __name__ == '__main__':
    app.run()