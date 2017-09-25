// Experiment Javascript


function makeTable(jsondata){
    table = jQuery("#experimental-data"), row = null, data = null;
    console.log(jsondata);
    makeHeaders(jsondata, table);
    $.each(jsondata, function(key, obj){
        row = $('<tr></tr>'); // Create a new row
        $.each(obj, function(k, v){
            $('<td></td>',{text:v}).appendTo(row);
        });
        row.appendTo(table);
    });
}

function makeHeaders(jsondata, table){
    console.log(jsondata);
    row = $('<tr></tr>');
    for (prop in jsondata[0]){
        console.log(prop);
        $('<th></th>',{text:prop}).appendTo(row);
    }
    row.appendTo(table);


}
$.ajax({
    url: "/app/experimentjs/"+id,
    dataType: 'json',
    success: function(data) {
        console.log(data);
        makeTable(data);
    }
});
