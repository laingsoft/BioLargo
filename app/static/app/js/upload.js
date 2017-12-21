var container = document.getElementById('experiment-data');
var col_headers;
var col_validators;
var hot;
var options = {data: [['']],
    rowHeaders: true,
    contextMenu: true,
    preventOverflow: 'horizontal',
    manualRowMove: true,
}

$("document").ready(function(){

    form = $("input[type=radio]:checked").val()
    if (form){
        $("#exp_data").append($("#" + form))
    }

});


// will use default validator for dates?
var VALIDATORS = {
    "INT" : /\d*/,
    "FLOAT" : /\d*(\.\d+)?/,
    "STRING" : /.*/
};

$('#add-row').click(function() {
    hot.alter('insert_row', 1);
});

$('#template-select').change(function() {
    get_template($(this).val());
});

$("#exp-form").submit(function(e) {

    headers = hot.getColHeader();
    data = hot.getData();

    metadata = $(".metadata")

    metadata_values = {}

    for (var i = 0 ; i < metadata.length; i++){
        key = metadata[i].placeholder
        metadata_values[key] = metadata[i].value
    }

    var parsed = [];
    for (row = 0; row < data.length; row++) {
        d = {};
        for (h = 0; h < headers.length; h++) {
            d[headers[h]] = data[row][h];
        }
        parsed.push(d);
    }

    $("#id_exp_data-json").val(JSON.stringify({'metadata': metadata_values, 'data': parsed}));
});

function update_metadata(fields){
    var container = $("#metadata-fields")
    container.empty()
    for (i=0; i < fields.length; i++){
        container.append("<label for='id_"+ fields[i][0] +"'>"+ fields[i][0] + "</label><input id='id_" + fields[i][0] + "' placeholder='"+ fields[i][0] + "' class='form-control metadata'></input>")
    }
}

function update_data_fields(fields){
    try {
        hot.destroy() // destroy table
    }
    catch(TypeError){
        // do nothing if the hot instance doesn't exist.
    }

    col_headers = fields.map(x => x[0]); // set headers.
    col_validators = fields.map(x => {data:VALIDATORS[x[1]]}); // set validators

    options.colHeaders = col_headers;
    options.columns = col_validators;

    hot = new Handsontable(container, options);

}


$("input[type=radio]").change(function() {
    $("#hidden_fields").append($("#exp_data > .form"))
    $("#exp_data").append($("#" + this.value))
});

//~ Autocomplete initalization

$('#id_exp-project').selectize({
    preload: true,
    placeholder: 'Select a project',
});

$('#id_exp-tags').selectize({
    preload: true,
    placeholder: 'Add Tags',
    plugins: ['remove_button', "restore_on_backspace"],
    delimiter: ',',
    create: function(input, callback){
        csrf_token = $("input[name=csrfmiddlewaretoken]").val()
        $.post("/app/create_tag/",
            {'csrfmiddlewaretoken': csrf_token, 'tag': input },
            callback({'value' : input, 'text' : input })
            );
    },
    createOnBlur: true,
    persist: true,
    hideSelected: true,
});

var template_select = $('#id_exp_data-template').selectize({
    placeholder: 'Select a template',
    onChange: function(value){
        $.get('/app/get_template', {name: value}, function(result){
            update_metadata(result.fields);
            update_data_fields(result.metadata);
        });
    }
});
