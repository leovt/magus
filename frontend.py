from flask import Flask, request, abort
from flask_restful import Resource, Api

from sample_data import TEST_CANTONS

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

class Table(Resource):
    def get(self, fq_name):
        if fq_name != 'test.cantons':
            abort(404)
        return TEST_CANTONS

api.add_resource(Table, '/tables/<string:fq_name>/json')

@app.route('/tables/<string:fq_name>')
def table_html(fq_name):
    if fq_name != 'test.cantons':
        abort(404)

    table = TEST_CANTONS

    thead = ''.join('<th>'+col['name']+'</th>' for col in table['columns'])
    tbody = '\n'.join('<tr>' + ''.join('<td>'+str(field)+'</td>' for field in row)+'</tr>' for row in table['data'])

    return f'''<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>{table['name']}</title>
    <link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/1.10.19/css/jquery.dataTables.css">
    <link rel="stylesheet" href="style.css">
    <script
    			  src="https://code.jquery.com/jquery-3.3.1.js"
    			  integrity="sha256-2Kok7MbOyxpgUVvAk/HJ2jigOSYS2auK4Pfzbm7uH60="
    			  crossorigin="anonymous"></script>
    <script type="text/javascript" charset="utf8" src="https://cdn.datatables.net/1.10.19/js/jquery.dataTables.js"></script>
    <script>
$(document).ready( function () {{
     $('#table_id').DataTable({{'paging': false}});
  }});
    </script>
  </head>
  <body>
<table id="table_id" class="display">
    <thead>
      <tr>{thead}</tr>
    </thead>
    <tbody>
        {tbody}
    </tbody>
</table>
</body>
</html>'''
