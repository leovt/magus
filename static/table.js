$(document).ready( function () {
  var tr = document.querySelector('tr');
  var oReq = new XMLHttpRequest();
  oReq.addEventListener("load", function(){
    table = JSON.parse(this.response);
    table.columns.forEach(function(col){
      var th = document.createElement('th');
      th.textContent = col.name;
      tr.appendChild(th);
    })
    $('#table_id').DataTable({
      'ajax': '../tables/test.cantons/json',
      'paging': false
    });
  });
  oReq.open("GET", '../tables/test.cantons/json');
  oReq.send();
} );
