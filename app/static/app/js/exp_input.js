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
    cell = rows[i].insertCell(rows[i].cells.length - 2);
    if (i === 0){
      cell.innerHTML = "<textarea class='header-box' required></textarea>";
    }
    else {
      cell.innerHTML = "<input class='input-form'></input>";
    }
  }
}

function parse_input(){
    var attributes = [];
    var table = document.getElementById('data');
    //~ get headers
    headers = table.rows[0].cells
    
    for (var i = 0; i < headers.length -1; i++){
        var inputField = headers[i].getElementsByClassName("textarea")[0];
        
        if(inputField){
            attributes.push(inputField.value);
        }
        else {
            attributes.push(headers[i].innerText);
        }
    }
    
    exp_data = [];
    
    for (i = 1; i < table.rows.length - 1; i++) {
        var data = {};
        for (var j = 0; j < attributes.length; j++) {
            data[attributes[j]] = table.rows[i].cells[j].getElementsByClassName("input-cell")[0].value;
        }
        
        exp_data.push(data);
    }
    
    hidden_field = document.getElementById("id_exp_data-json");
    hidden_field.value = JSON.stringify(exp_data);
    
}
$('.delete-row').click(function () {
  $(this).parents('tr').detach();
});
