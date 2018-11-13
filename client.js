var selection;
var start_drag_event;

function startDrag(evt){
  console.log(evt.target);
  console.log(evt.target.parentElement);
  if (evt.target.parentElement.classList.contains('icon')) {
    selection = evt.target.parent;
    start_drag_event = evt;
  } else {
    selection = null;
  }
}

function moveDrag(evt){
  console.log(selection.transform)
}
