import sqlite3

from flask_jwt import jwt_required
from flask_restful import Resource, reqparse


class Item(Resource):

    @jwt_required()
    def get(self, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT * FROM items WHERE name=?"
        results = cursor.execute(query, (name,))
        row = results.fetchone()
        connection.close()

        if row:
            return {'item': {'name': row[0], 'price': row[1]}}

        return {'message': 'Item not found'}, 404

    def post(self, name):

        if next(filter(lambda x: x['name'] == name, items), None) is not None:
            return {'message': f"An item with {name} already exists."}, 400

        data = self._check_and_get_parser()

        item = {'name': name, 'price': data['price']}
        items.append(item)
        return item, 201

    def delete(self, name):
        global items
        items = list(filter(lambda x: x['name'] != name, items))
        return {'message': 'Item deleted'}

    def put(self, name):
        data = self._check_and_get_parser()

        item = next(filter(lambda x: x['name'] == name, items), None)
        if item is None:
            item = {'name': name, 'price': data['price']}
            items.append(item)
        else:
            item.update(data)

        return item

    def _check_and_get_parser(self):
        parser = reqparse.RequestParser()
        parser.add_argument(
            'price',
            type=float,
            required=True,
            help='This field cannot be left blank!')

        return parser.parse_args()


class ItemList(Resource):
    def get(self):
        return items, 200
