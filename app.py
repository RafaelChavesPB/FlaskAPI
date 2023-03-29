from flask import Flask, request
from flask_smorest import abort
from db import stores, items
import uuid

app = Flask(__name__)

@app.get('/store')
def get_stores():
    return {"stores": stores}, 200


@app.post('/store')
def create_store():
    data = request.get_json()
    store_id = uuid.uuid1().hex
    new_store = {**data, "id": store_id}
    stores[store_id] = new_store
    return new_store, 201


@app.get('/store/<string:store_id>')
def get_store(store_id):
    try:
        return stores[store_id]
    except KeyError:
        return {"message": "Store not found"}, 404


@app.post('/item')
def create_item():
    data = request.get_json()
    if data['store_id'] not in stores:
        return {"message": "Store not found"}, 404
    item_id = uuid.uuid1().hex
    new_item = {**data, "id": item_id}
    items[item_id] = new_item
    return new_item

@app.get('/item')
def get_items():
    return items, 200

@app.get('/item/<string:item_id>')
def get_item(item_id):
    if item_id not in items:
        abort(404, message="Item not found")
    return items[item_id]