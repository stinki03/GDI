
from flask import Flask, request
app = Flask(__name__)
contacts = {}
@app.route('/contacts', methods=['POST'])
def create():
 data = request.get_json()
 id = str(len(contacts)+1)
 contacts[id] = data
 data["id"] = id
 return data
@app.route('/contacts', methods=['GET'])
def list_all():
 return list(contacts.values())
@app.route('/contacts/<id>', methods=['PUT'])
def update(id):
 data = request.get_json()
 contacts[id].update(data)
 contacts[id]["id"] = id
 return contacts[id]
@app.route('/contacts/<id>', methods=['DELETE'])
def delete(id):
 del contacts[id]
 return '', 204
if __name__ == '__main__':
 app.run()
