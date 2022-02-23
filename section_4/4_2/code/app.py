from flask import Flask, request
from flask_jwt import JWT, jwt_required
from flask_restful import Resource, Api

from security import authenticate, identity

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

        request_data = request.get_json()
        item = {'name': name, 'price': request_data['price']}
        items.append(item)
        return item, 201


class ItemList(Resource):
    def get(self):
        return items, 200


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/item')

app.run(port=5000, debug=True)
