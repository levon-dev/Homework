from json import JSONEncoder
from flask import Flask, json, jsonify, request

from model.twit import Twit

twits = []

app = Flask(__name__)

class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Twit):
            return{'body': obj.body, 'author': obj.author}
        else:
            return super().default(obj)


app.json_encoder = CustomJSONEncoder

@app.route('/ping', methods=['GET'])
def ping():
  return jsonify({'response': 'pong'})

@app.route('/twit', methods=['POST'])
def create_twit():
    '''{"body": "Hello World!", "author": "@aqaguy"}
    '''
    twit_json = request.get_json()
    twit = Twit(twit_json['body'], twit_json['author'])
    twits.append(twit)
    return jsonify({'status': 'success'})

@app.route('/twit', methods=['GET'])
def read_twits():
    return jsonify({'twits': twits})

@app.route('/twit/delete', methods=['POST'])
def delete_twit():
    '''{"index": 0}'''
    twit_json = request.get_json()
    index = twit_json['index']
    if index < 0 or index >= len(twits):
        return jsonify({'status': 'error', 'message': 'index out of range'}), 404
    twits.pop(index)
    return jsonify({'status': 'success'})

@app.route('/twit/update', methods=['POST'])
def update_twit():
    '''{"index": 0, "body": "новый текст", "author": "@new"}'''
    twit_json = request.get_json()
    index = twit_json['index']
    if index < 0 or index >= len(twits):
        return jsonify({'status': 'error', 'message': 'index out of range'}), 404
    if 'body' in twit_json:
        twits[index].body = twit_json['body']
    if 'author' in twit_json:
        twits[index].author = twit_json['author']
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(debug=True)
