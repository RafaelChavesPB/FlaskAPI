from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import ItemSchema, ItemUpdateSchema
import uuid

from db import items, stores

blp = Blueprint("Items", __name__, description="Operating on items")


@blp.route('/item')
class ItemList(MethodView):
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        return list(items.values())

    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, data):
        if data['store_id'] not in stores:
            abort(404, message="Store not found")

        for item in items.values():
            if item['name'] == data['name'] and item['store_id'] == data['store_id']:
                abort(400, message="Item already exists.")

        item_id = uuid.uuid1().hex
        new_item = {**data, "id": item_id}
        items[item_id] = new_item
        return new_item


@blp.route('/item/<string:item_id>')
class Item(MethodView):
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        if item_id not in items:
            abort(404, message="Item not found.")
        return items[item_id]

    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, data, item_id):
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
