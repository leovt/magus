from flask import Flask, request, abort
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

flow_items = {
    'source': {
      'icon': 'table',
      'label': 'work.source',
      'x': 40,
      'y': 20,
      'succ': ['select'],
      'pred': []
    },
    'select': {
      'icon': 'task',
      'label': 'query on source',
      'x': 120,
      'y': 20,
      'succ': ['result'],
      'pred': ['source']
    },
    'result': {
      'icon': 'table',
      'label': 'work.result',
      'x': 200,
      'y': 20,
      'succ': [],
      'pred': ['select']
    }
}

# curl 127.0.0.1:5000/flowitems/source -X PUT -d "{"""x""": 20, """y""": 30}" -H "Content-Type: application/json"

class FlowItem(Resource):
    def get(self, item_id):
        return {item_id: flow_items[item_id]}

    def put(self, item_id):
        template = {
            'x': int,
            'y': int,
        }
        if not request.json:
            abort(400)
        if not item_id in flow_items:
            abort(404)
        for key, value in request.json.items():
            if type(value) is not template.get(key):
                abort(400)
        flow_items[item_id].update(request.json)
        return '', 204 # no content

class FlowItemList(Resource):
    def get(self):
        return flow_items

api.add_resource(FlowItem, '/flowitems/<string:item_id>')
api.add_resource(FlowItemList, '/flowitems')
