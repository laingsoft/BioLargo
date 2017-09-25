var container = document.getElementById('data-table');
var templates;

var hot = new Handsontable(container, {
    data : [[]],
    rowHeaders:true,
    colHeaders: true,
    contextMenu: true,
});

window.onload = get_template(null)

function load_template(template) {
    fields = template.fields;
    col = fields.map(function(field) {
        {data : field};
        });
    hot.updateSettings({colHeaders:fields, columns: col});
}

function get_template(template_name) {
    $.get("/app/get_template", {template : template_name}, load_template);
}

function parse_data() {
    headers = hot.getColHeader();
    data = hot.getData();
    
    var parsed = [];
    for (row = 0; row < data.length; row++){
        d = {};
        for (h = 0; h < headers.length; h++){
            d[headers[h]] = data[row][h];
        }
        parsed.push(d);
    }
    
    $("#id_exp_data-json").val(JSON.stringify(parsed));
};
    
$('#add-var').click(function(){
    name = prompt("Please Enter Variable Name");
    if (name !== 'null') {
        headers = hot.getColHeader();
        headers.splice(-1,0, name);
        col.splice(-1,0, {data : name})
        hot.updateSettings({colHeaders : headers});
    }
});

$('#add-row').click(function(){
    hot.alter('insert_row', 1);
    });

$('#template-select').change(function(){
    get_template($(this).val());
    });

$('#template-save').click(function(){
    prompt("this does something");
    });
