import sqlite3
from flask_jwt import jwt_required
from flask_restful import Resource, reqparse

class Item (Resource):
    parser= reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help = "This filed can't be blank"
        )

    @jwt_required()
    def get(self, name):
      item = self.find_by_name(name)
      if item:
          return item 
      return {'msg' : "Item not found"}, 404


    @classmethod
    def find_by_name(cla, name):
        
        conection = sqlite3.connect('data.db')
        cursor = conection.cursor()

        query = "SELECT * FROM items WHERE item=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        conection.close()

        if row:
            return {'item': {"name": row[0], "price": row[1]}}, 200

    @classmethod
    def post (cls, name):
        if cls.find_by_name(name):
            return {'Msg': "Item with name '{}' already exits.".format(name)}, 400

        data = Item.parser.parse_args()
        item = {'name': name, 'price': data['price']}

        try:
            cls.insert(item)
        except:
            return {"msg": "Koi glti ho gyi bhai!"}, 500
        return item, 201

    @classmethod
    def insert(cls, item):
        conection = sqlite3.connect('data.db')
        cursor = conection.cursor()

        query = "INSERT INTO items VALUES(?, ?)"
        cursor.execute(query, (item['name'], item['price'],))

        conection.commit()
        conection.close()


    def delete(self, name):
        conection = sqlite3.connect('data.db')
        cursor = conection.cursor()

        query = "DELETE FROM items WHERE item=?"
        cursor.execute(query, (name,))

        conection.commit()
        conection.close()
        return {'msg': 'Item deleted'}

    
    @classmethod
    def put(cls, name):
        data = Item.parser.parse_args()
        item = cls.find_by_name(name)
        update_item = {'name': name, 'price': data['price']}
        if item:
            try:
                cls.update(update_item)
            except:
                return {"msg": "Koi glti ho gyi bhai update krte time!"}, 500
        else:
            try:
                cls.insert(update_item)
            except:
                return {"msg": "Koi glti ho gyi bhai update krte time!"}, 500
        return update_item, 201

    @classmethod
    def update(cls,item):
        conection = sqlite3.connect('data.db')
        cursor = conection.cursor()

        query = "UPDATE items SET price=? WHERE item=?"
        cursor.execute(query, (item['price'],item['name'],))

        conection.commit()
        conection.close()

class ItemList (Resource):
    def get(self):
        conection = sqlite3.connect('data.db')
        cursor = conection.cursor()
        
        query = "SELECT * FROM items"
        result = cursor.execute(query)
        items = []
        for row in result:
            items.append({'name': row[0], 'price': row[1]})

        conection.close()
        return {'items': items}
