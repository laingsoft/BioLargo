//~ from https://codepen.io/ashblue/pen/mCtuA

var $TABLE = $('#input-table');

function add_row() {
  var $clone = $TABLE.find('tr.hide').clone(true).removeClass('hide table-line');
  $TABLE.find('table').append($clone);
}

function add_col() {
  var table = document.getElementById('data');
  var rows = table.rows;

  for (var i = 0; i < rows.length; i++){
    cell = rows[i].insertCell(rows[i].cells.length - 1);
    if (i === 0){
      cell.innerHTML = "<input required></input>";
    }
    else {
      cell.innerHTML = "<input></input>";
    }
  }
}

$('.delete-row').click(function () {
  $(this).parents('tr').detach();
});

