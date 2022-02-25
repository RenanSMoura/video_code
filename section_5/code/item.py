import sqlite3

from flask_jwt import jwt_required
from flask_restful import Resource, reqparse


class Item(Resource):

    @jwt_required()
    def get(self, name):
        item = self.find_by_name(name)
        if item:
            return item

        return {'message': 'Item not found'}, 404

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT * FROM items WHERE name=?"
        results = cursor.execute(query, (name,))
        row = results.fetchone()
        connection.close()

        if row:
            return {'item': {'name': row[0], 'price': row[1]}}

    def post(self, name):

        if self.find_by_name(name):
            return {'message': f"An item with {name} name already exists."}, 400

        data = self._check_and_get_parser()

        item = {'name': name, 'price': data['price']}

        try:
            self.insert(name, data['price'])
        except:
            return {'Message': 'An error occurred inserting the item'}, 500

        return item, 201

    @classmethod
    def insert(cls, name, price):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "INSERT INTO items VALUES(?,?)"
        cursor.execute(query, (name, price))

        connection.commit()
        connection.close()

    def put(self, name):
        data = self._check_and_get_parser()

        item = self.find_by_name(name)
        if item is None:
            self.insert(name, data['price'])
            item = {'name': name, 'price': data['price']}
        else:
            self.update_item(name, data['price'])
            item = self.find_by_name(name)

        return item

    @classmethod
    def update_item(cls, name, price):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "UPDATE items SET price=? WHERE name=?"
        cursor.execute(query, (price, name))
        connection.commit()
        connection.close()

    def delete(self, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "DELETE FROM items WHERE name=?"
        cursor.execute(query, (name,))
        connection.commit()
        connection.close()
        return {'message': 'Item deleted'}

    @classmethod
    def _check_and_get_parser(cls):
        parser = reqparse.RequestParser()
        parser.add_argument(
            'price',
            type=float,
            required=True,
            help='This field cannot be left blank!')

        return parser.parse_args()


class ItemList(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT * FROM items"
        items = []

        for row in cursor.execute(query):
            items.append({
                'name': row[0],
                'price': row[1]
            })

        return items, 200
