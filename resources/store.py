from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
import uuid

from db import stores

blp = Blueprint("Stores", __name__, description = "Operating on stores")

@blp.route('/store')
class StoreList(MethodView):
    def get(self):
        return {"stores": list(stores.values())}, 200

    def post(self):
        data = request.get_json()
        if 'name' not in data:
            abort(400, message="Bad request. Ensure 'name' are included in the JSON payload.")
        for store in stores.values():
            if store['name'] == data['name']:
                abort(400, message="Store already exists.")
        store_id = uuid.uuid1().hex
        new_store = {**data, "id": store_id}
        stores[store_id] = new_store
        return new_store, 201


@blp.route('/store/<string:store_id>')
class Store(MethodView):
    def get(self, store_id):
        if store_id not in stores:
            return abort(404, message="Store not found")
        return stores[store_id]

    def put(self, store_id):
        data = request.get_json()
        if 'name' not in data:
            abort(400, message="Bad request. Ensure 'name' are included in the JSON payload.")
        if store_id not in stores:
            abort(404, messge="Store not found.")
        store = stores[store_id]
        store['name'] = data['name']
        return store

    def delete(self, store_id):
        if store_id not in stores:
            return abort(404, message="Store not found.")
        del stores[store_id]
        return {'message': 'Store deleted.'}
