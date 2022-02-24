from flask import Flask
from flask_jwt import JWT, jwt_required
from flask_restful import Resource, Api, reqparse

from security import authenticate, identity
from user import UserRegister

app = Flask(__name__)
app.secret_key = "iahjueoh801728ahuo12y"
api = Api(app)
jwt = JWT(app, authenticate, identity)

items = []


class Item(Resource):

    @jwt_required()
    def get(self, name):
        item = next(filter(lambda x: x['name'] == name, items), None)
        return {'item': item}, 200 if item else 404

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


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/item')
api.add_resource(UserRegister, '/register')

app.run(port=5000, debug=True)
