var container = document.getElementById('data-table');
var templates;

var hot = new Handsontable(container, {
    data : [[]],
    rowHeaders:true,
    colHeaders: true,
    contextMenu: true,
    preventOverflow: 'horizontal',
});

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
    }
});


window.onload = get_template($('#template-select').val())

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
    
$('#var-save').click(function(){
    name = $('#var-name').val();
    if (name) {
        headers = hot.getColHeader();
    
        headers.splice(-1,0, name);
        col.splice(-1,0, {data : name})
        hot.updateSettings({colHeaders : headers});
    }
    $('#var_name').val('');
    $('#var_modal').modal('hide')
});

$('#add-row').click(function(){
    hot.alter('insert_row', 1);
    });

$('#template-select').change(function(){
    get_template($(this).val());
    });

$('#template-save').click(function(){
    name = $('#template-name').val();
    
    if (name) {
        $.post("/app/save_template", 
        JSON.stringify({name : name, fields : hot.getColHeader()}));
        }
        
    $('#template_name').val('');
    $('#template_modal').modal('hide')
    });
