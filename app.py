from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

stores=[
    {
        'name': 'My Store',
        'item': [{
            'name': 'First item',
            'price': 12.99
        }]
    }
]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/store', methods=['POST'])
def create_store():
   request_data = request.get_json()
   new_store ={
       'name': request_data['name'],
       'item': []
   }
   stores.append(new_store)
   return jsonify({'stores':stores})

@app.route('/store/<string:name>', methods=['GET'])
def get_store(name):
    for item in stores:
        if (name == item['name']):
            return jsonify(item)
    return jsonify({'massage': 'Store not found'})

@app.route('/store', methods=['GET'])
def get_stores():
    return jsonify({'stores':stores})

@app.route('/store/<string:name>/item', methods=['POST'])
def create_items_in_store(name):
    request_data = request.get_json()
    for item in stores:
       if (name == item['name']):
           new_item ={
               'name': request_data['name'],
               'price': request_data['price']
           }
           item['item'].append(new_item)
           return jsonify(new_item)
    return jsonify({'massage':'Store not found'})

@app.route('/store/<string:name>/item', methods=['GET'])
def get_items_in_store(name):
    for item in stores:
        if (name == item['name']):
            return jsonify({'items': item['item']})
    return jsonify({'massage': 'Store not found'})


app.run(port=5000)