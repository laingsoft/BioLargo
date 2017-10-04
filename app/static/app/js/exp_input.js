var container = document.getElementById('data-table');
var data = [['']];
var templates;
var col;
var hot;
var csrftoken;

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);

            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function load_template(template) {
    fields = template.fields;
    col = fields.map(function(field) {
        return {
            data: field
        };
    });
    
    hot.updateSettings({
        colHeaders: fields,
        columns: col
    });
}

function get_template(template_name) {
    $.get("/app/get_template", {
        template: template_name
    }, load_template);
}

function parse_data() {
    headers = hot.getColHeader();
    data = hot.getData();

    var parsed = [];
    for (row = 0; row < data.length; row++) {
        d = {};
        for (h = 0; h < headers.length; h++) {
            d[headers[h]] = data[row][h];
        }
        parsed.push(d);
    }

    $("#id_form-json").val(JSON.stringify(parsed));
};

function save_template() {
    name = $('#template-name').val();

    if (name) {
        $.post("/app/save_template",
            JSON.stringify({
                name: name,
                fields: hot.getColHeader()
            }));
    }

    $('#template-name').val('');
    $('#template-modal').modal('hide')
}

function add_var() {
    name = $('#var-name').val();

    headers = hot.getColHeader();
    headers = headers.filter(function(e) {
        return e;
    });
    
    if (headers.length === 0){
        col = []
    }
    headers.push(name);

    col.push({data: name
    })
    hot.updateSettings({
        colHeaders: headers,
        columns: col
    });
    
    $('#var-name').val('');
    $('#var-modal').modal('hide')
}


$(document).ready(function(){
    
    hot = new Handsontable(container, {
    data: data,
    rowHeaders: true,
    colHeaders: true,
    contextMenu: true,
    preventOverflow: 'horizontal',
    manualColumnMove: true,
    manualRowMove: true,
    });
    
    csrftoken = getCookie('csrftoken');
    $.ajaxSetup({
    beforeSend: function(xhr, settings) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    });
    
    get_template($('#template-select').val())
    
    $('#add-row').click(function() {
    hot.alter('insert_row', 1);
    });

    $('#template-select').change(function() {
    get_template($(this).val());
    });


    $("input[type=radio]").change(function(){
        var current = $("#form > .upload_fields");
        $("#form").append($("#hidden_fields > .upload_fields"));
        $("#hidden_fields").append(current);
    });
})

