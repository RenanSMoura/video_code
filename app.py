from flask import Flask, jsonify, request

app = Flask(__name__)

stores = [
    {
        'name': 'My Wonderful Store',
        'items': [
            {
                'name': 'My Item',
                'price': 13.93
            }
        ]
    }
]


@app.route("/stores")
def get_store_list():
    return jsonify({'stores': stores})


@app.route("/store", methods=["POST"])
def create_store():
    request_data = request.get_json()
    new_store = {
        'name': request_data['name'],
        'items': []
    }
    stores.append(new_store)
    return jsonify(new_store)


@app.route("/store/<string:name>")
def get_store(name):
    print(name)
    for store in stores:
        print(f"store ${store}")
        if store['name'] == name:
            return jsonify(store)
        else:
            return jsonify({'message': 'store not found'})
    pass


@app.route("/store/<string:name>/item", methods=["POST"])
def create_store_item(name):
    for store in stores:
        if store['name'] == name:
            request_data = request.get_json()
            new_item = {
                'name': request_data['name'],
                'price': request_data['price']
            }
            store['items'].append(new_item)
            return jsonify(new_item)

    return jsonify({'message': 'store not found'})


@app.route("/store/<string:name>/item")
def get_store_item(name):
    for store in stores:
        if store['name'] == name:
            return jsonify({'items': store['items']})
        else:
            return jsonify({'message': 'store not found'})
