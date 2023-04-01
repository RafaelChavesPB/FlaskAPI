from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
import uuid

from db import items, stores

blp = Blueprint("Items", __name__, description="Operating on items")


@blp.route('/item')
class ItemList(MethodView):
    def get(self):
        return {"items": list(items.values())}, 200

    def post(self):
        data = request.get_json()
        if 'store_id' not in data or 'name' not in data or 'price' not in data:
            abort(400, message="Bad request. Ensure 'price', 'store_id', and 'name' are included in the JSON payload.")

        if data['store_id'] not in stores:
            abort(404, message="Store not found")

        for item in items.values():
            if item['name'] == data['name'] and item['store_id'] == data['store_id']:
                abort(400, message="Item already exists.")

        item_id = uuid.uuid1().hex
        new_item = {**data, "id": item_id}
        items[item_id] = new_item
        return new_item, 201


@blp.route('/item/<string:item_id>')
class Item(MethodView):
    def get(self, item_id):
        if item_id not in items:
            abort(404, message="Item not found.")
        return items[item_id]

    def put(self, item_id):
        data = request.get_json()
        if 'store_id' not in data or 'name' not in data or 'price' not in data:
            abort(400, message="Bad request. Ensure 'price', 'store_id', and 'name' are included in the JSON payload.")

        if data['store_id'] not in stores:
            abort(404, message="Store not found.")

        if item_id not in items:
            abort(404, message="Item not found.")

        item = items[item_id]
        item.update(data)
        return item, 201

    def delete(self, item_id):
        if item_id not in items:
            abort(404, message="Item not found")
        del items[item_id]
        return {'message': 'Item deleted.'}
