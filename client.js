var flow_json = {
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
  };


function setup_dragdrop(){
  var selection;
  var mousepos_off_x;
  var mousepos_off_y;
  var svg = document.querySelector('svg');

  function cursorPoint(evt){
    var pt = svg.createSVGPoint();
    pt.x = evt.clientX; pt.y = evt.clientY;
    return pt.matrixTransform(svg.getScreenCTM().inverse());
  }

  function startDrag(evt){
    if (evt.button != 0) {return;}
    if (evt.target.parentElement.classList.contains('icon')) {
      selection = evt.target.parentElement;
      var pt = cursorPoint(evt);
      mousepos_off_x = pt.x - selection.transform.baseVal.getItem(0).matrix.e;
      mousepos_off_y = pt.y - selection.transform.baseVal.getItem(0).matrix.f;
    } else {
      selection = null;
    }
  }

  function moveDrag(evt){
    if (selection) {
      var pt = cursorPoint(evt);
      moveIcon(selection.id, pt.x-mousepos_off_x, pt.y-mousepos_off_y);

    }
  }

  function endDrag(evt){
    selection = null;
  }

  svg.addEventListener('mousedown', startDrag);
  svg.addEventListener('mousemove', moveDrag);
  svg.addEventListener('mouseup', endDrag);
};

document.addEventListener("DOMContentLoaded", setup_dragdrop);

function moveIcon(id, x, y){
  var icon = document.querySelector('#'+id);
  flow_json[id].x = x;
  flow_json[id].y = y;
  icon.transform.baseVal.getItem(0).setTranslate(x,y);
  flow_json[id].succ.forEach(function(succ){
    moveArrow(id+'-'+succ, flow_json[id].x, flow_json[id].y, flow_json[succ].x, flow_json[succ].y);
  });
  flow_json[id].pred.forEach(function(pred){
    moveArrow(pred+'-'+id, flow_json[pred].x, flow_json[pred].y, flow_json[id].x, flow_json[id].y);
  });
}

function addIcon(id, x, y, symbol, label){
  var svg = document.querySelector('svg');
  var group = document.createElementNS("http://www.w3.org/2000/svg", 'g');
  svg.appendChild(group);
  group.id = id;
  group.setAttribute('transform', 'translate(0,0)');
  group.setAttribute('class', 'icon');
  group.transform.baseVal.getItem(0).setTranslate(x,y);
  var use = document.createElementNS("http://www.w3.org/2000/svg", 'use');
  use.setAttribute('href', "#"+symbol);
  text = document.createElementNS("http://www.w3.org/2000/svg", 'text');
  text.setAttribute('class', 'icon');
  text.setAttribute('text-anchor', "middle");
  text.setAttribute('x', '15');
  text.setAttribute('y', '42');
  text.textContent = label;
  group.appendChild(use);
  group.appendChild(text);
}

function addArrow(id, x1, y1, x2, y2){
  var svg = document.querySelector('svg');
  var path = document.createElementNS("http://www.w3.org/2000/svg", 'path')
  path.id = id;
  path.setAttribute('class', 'arrow');
  path.setAttribute('marker-start', "url(#arrowtail)");
  path.setAttribute('marker-end', "url(#arrowhead)");
  svg.appendChild(path);
  moveArrow(id, x1, y1, x2, y2);
}

function moveArrow(id, x1, y1, x2, y2){
  var path = document.querySelector('#'+id)
  path.setAttribute('d', `M${x1+40} ${y1+15} L${x1+50} ${y1+15} L${x2-20} ${y2+15} L${x2-10} ${y2+15}`);
}


function onAddIcon(){
  addIcon('random', 100, 100, 'table', 'random');
}


function loadJSON(){
  $('.icon').remove()

  Object.entries(flow_json).forEach(function([key, value]){
    addIcon(key, value.x, value.y, value.icon, value.label);
  })

  Object.entries(flow_json).forEach(function([key, value]){
    value.succ.forEach(function(succ){
      addArrow(key+'-'+succ, value.x, value.y, flow_json[succ].x, flow_json[succ].y);
    })
  })
}
