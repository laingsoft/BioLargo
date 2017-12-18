var container = document.getElementById('experiment-data');
var templates;
var col;
var hot;

// will not validate dates because format can vary. Will leave that to the server to parse and reformat if needed.
var VALIDATORS = {
    "INT" : /\d*/,
    "FLOAT" : /\d*(\.\d+)?/,
    "STRING" : /.*/
};


hot = new Handsontable(container, {
data: [['']],
rowHeaders: true,
colHeaders: col,
contextMenu: true,
preventOverflow: 'horizontal',
manualColumnMove: true,
manualRowMove: true,
});


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

