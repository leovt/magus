var selection;
var start_drag_event;

function startDrag(evt){
  console.log(evt.target);
  console.log(evt.target.parentElement);
  if (evt.target.parentElement.classList.contains('icon')) {
    selection = evt.target.parentElement;
    start_drag_event = evt;
  } else {
    selection = null;
  }
}

function moveDrag(evt){
  if (selection) {
    selection.transform.baseVal.getItem(0).setTranslate(evt.clientX, evt.clientY);
  }
}

function endDrag(evt){
  selection = null;
}
