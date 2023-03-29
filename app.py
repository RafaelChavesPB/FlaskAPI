from flask import Flask, request
from flask_smorest import abort
from db import stores, items
import uuid

app = Flask(__name__)


@app.get('/store')
def get_stores():
    return {"stores": list(stores.values())}, 200


@app.post('/store')
def create_store():
    data = request.get_json()
    if 'name' not in data:
        abort(400, message = "Bad request. Ensure 'name' are included in the JSON payload.")
    for store in stores.values():
        if store['name'] == data['name']:
            abort(400, message = "Store already exists.")
    store_id = uuid.uuid1().hex
    new_store = {**data, "id": store_id}
    stores[store_id] = new_store
    return new_store, 201


@app.get('/store/<string:store_id>')
def get_store(store_id):
    if store_id not in stores:
        return abort(404, message = "Store not found")
    return stores[store_id]


@app.post('/item')
def create_item():
    data = request.get_json()
    if 'store_id' not in data or 'name' not in data or 'price' not in data:
        abort(400, message = "Bad request. Ensure 'price', 'store_id', and 'name' are included in the JSON payload.")
    
    if data['store_id'] not in stores:
        abort(404, message = "Store not found")

    for item in items.values():
        if item['name'] == data['name'] and item['store_id'] == data['store_id']:
            abort(400, message = "Item already exists.")

    item_id = uuid.uuid1().hex
    new_item = {**data, "id": item_id}
    items[item_id] = new_item
    return new_item, 201


@app.get('/item')
def get_items():
    return {"items": list(items.values())}, 200


@app.get('/item/<string:item_id>')
def get_item(item_id):
    if item_id not in items:
        abort(404, message="Item not found")
    return items[item_id]
