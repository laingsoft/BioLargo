var container = document.getElementById('experiment-data');
var col_headers;
var hot;

// will use default validator for dates?
var VALIDATORS = {
    "INT" : /\d*/,
    "FLOAT" : /\d*(\.\d+)?/,
    "STRING" : /.*/
};

var options = {data: [['']],
    rowHeaders: true,
    colHeaders: col_headers,
    contextMenu: true,
    preventOverflow: 'horizontal',
    manualRowMove: true,
}

hot = new Handsontable(container, options);


$('#add-row').click(function() {
hot.alter('insert_row', 1);
});

$('#template-select').change(function() {
    get_template($(this).val());
});

$("#exp-form").submit(function(e) {

    $("#template-select").attr("disabled")
    headers = hot.getColHeader();
    data = hot.getData();

    metadata = document.getElementById("metadata-fields");
    metadata = metadata.getElementsByTagName("input");

    metadata_values = {}

    for (var i = 0 ; i < metadata.length; i++){
        key = metadata[i].labels[0].textContent
        metadata_values[key] = metadata[i].value
    }

    console.log(metadata_values)

    var parsed = [];
    for (row = 0; row < data.length; row++) {
        d = {};
        for (h = 0; h < headers.length; h++) {
            d[headers[h]] = data[row][h];
        }
        parsed.push(d);
    }
    console.log(parsed)

    $("#id_data-json").val(JSON.stringify({'metadata': metadata_values, 'data': parsed}));
});


function update_metadata(fields){

}
