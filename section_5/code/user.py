import sqlite3

from flask_restful import Resource, reqparse


class User:
    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        connect = sqlite3.connect('data.db')
        cursor = connect.cursor()
        query = "SELECT * FROM users WHERE username=?"
        result = cursor.execute(query, (username,))
        row = result.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None
        connect.close()
        return user

    @classmethod
    def find_by_id(cls, _id):
        connect = sqlite3.connect('data.db')
        cursor = connect.cursor()
        query = "SELECT * FROM users WHERE id=?"
        result = cursor.execute(query, (_id,))
        row = result.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None
        connect.close()
        return user


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'username',
        type=str,
        required=True,
        help='Username field cannot be left blank!')
    parser.add_argument(
        'password',
        type=str,
        required=True,
        help='Password field cannot be left blank')

    @classmethod
    def post(cls):
        data = UserRegister.parser.parse_args()

        user = User.find_by_username(data['username'])

        if user:
            return {'Message': "User already exists"}, 400

        connect = sqlite3.connect('data.db')
        cursor = connect.cursor()
        insert_query = "INSERT INTO users VALUES(NULL,?,?)"
        cursor.execute(insert_query, (data['username'], data['password']))

        connect.commit()
        connect.close()
        return {'message': 'User created successfully'}, 201
