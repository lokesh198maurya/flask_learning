from flask import Flask, request
from flask_restful import Api, Resource, reqparse
from flask_jwt import JWT, jwt_required
from security import authentication, idenity


app = Flask(__name__)
app.secret_key = 'test_secret_key'
api = Api(app)
jwt = JWT(app, authentication, idenity) # /auth

items = []

class Item (Resource):
    parser= reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help = "This filed can't be blank"
        )

    @jwt_required()
    def get(self, name):
        item = next(filter(lambda ele: ele['name']==name, items), None)
        return {'item': item}, 200 if item else 404

    def post (self, name):
        if next(filter(lambda ele: ele['name']==name, items), None) is not None:
            return {'Msg': "Item with name '{}' already exits.".format(name)}, 400

        data = Item.parser.parse_args()
        item = {'name': name, 'price': data['price']}
        items.append(item)
        return item, 201

    def delete(self, name):
        global items
        items = list(filter(lambda ele: ele['name']!=name, items))
        return {'msg': 'Item deleted'}

    def put(self, name):
        data = Item.parser.parse_args()
        item = next(filter(lambda ele: ele['name']==name, items), None)
        if item:
            item.update(data)
        else:
            item = {'name': name, 'price': data['price']}
            items.append(item)
        return item, 201

class ItemList (Resource):
    def get(self):
        return {'items': items}

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')

app.run(port=5000, debug=True)