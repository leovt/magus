var selection;
var mousepos_off_x;
var mousepos_off_y;

function cursorPoint(evt){
  var svg = document.querySelector('svg');
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
