from flask import Flask, jsonify

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
    pass


@app.route("/store/<string:name>")
def get_store(name):
    pass


@app.route("/store/<string:name>/item", methods=["POST"])
def create_store_item():
    pass


@app.route("/store/<string:name>/item")
def get_store_item(name):
    pass


app.run(port=5000)
