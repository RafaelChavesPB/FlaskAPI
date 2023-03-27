from flask import Flask, request

app = Flask(__name__)

stores = [
    {
        "name": "FirstStore",
        "items": [
            {
                "name": "chair",
                "price": 12.29
            }
        ]
    }
]


@app.get('/store')
def get_stores():
    return {"stores": stores}, 200


@app.post('/store')
def create_store():
    data = request.get_json()
    new_store = {"name": data["name"], "items": []}
    stores.append(new_store)
    return new_store, 201


@app.get('/store/<string:name>')
def get_store(name):
    for store in stores:
        if store['name'] == name:
            return store
    return {"message": "Store not found"}, 404


@app.post('/store/<string:name>/item')
def create_item(name):
    for store in stores:
        if store['name'] == name:
            data = request.get_json()
            new_item = {"name": data["name"], "price": data["price"]}
            store['items'].append(new_item)
            return new_item, 201
    return {"message": "Store not found"}, 404


@app.get('/store/<string:name>/item/<string:item_name>')
def get_items(name, item_name):
    for store in stores:
        if store['name'] == name:
            for item in store['items']:
                if item['name'] == item_name:
                    return item, 200
            return {"message": "Item not found"}, 404
    return {"message": "Store not found"}, 404

if __name__ == '__main__':
    app.run(debug=True)
