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
      selection.transform.baseVal.getItem(0).setTranslate(pt.x-mousepos_off_x, pt.y-mousepos_off_y);
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

function onAddIcon(){
  addIcon('random', 100, 100, 'table', 'random');
}
