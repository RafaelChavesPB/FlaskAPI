from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import StoreSchema
import uuid

from db import stores

blp = Blueprint("Stores", __name__, description = "Operating on stores")

@blp.route('/store')
class StoreList(MethodView):
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        return  list(stores.values()), 200

    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def post(self, data):
        for store in stores.values():
            if store['name'] == data['name']:
                abort(400, message="Store already exists.")
        store_id = uuid.uuid1().hex
        new_store = {**data, "id": store_id}
        stores[store_id] = new_store
        return new_store


@blp.route('/store/<string:store_id>')
class Store(MethodView):
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        if store_id not in stores:
            return abort(404, message="Store not found")
        return stores[store_id]

    @blp.arguments(StoreSchema)
    @blp.response(200, StoreSchema)
    def put(self, data, store_id):
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
