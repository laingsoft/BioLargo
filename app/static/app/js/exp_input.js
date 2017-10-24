var container = document.getElementById('experiment-data');
var templates;
var col;
var hot;
var csrftoken;

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();

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
    
    metadata = document.getElementById("metadata-fields");
    metadata = metadata.getElementsByTagName("input");

    metadata_values = {}
    
    for (var i = 0 ; i < metadata.length; i++){
        metadata_values[metadata[i].name] = metadata[i].value
    }
    
    console.log(metadata_values);
    
    var parsed = [];
    for (row = 0; row < data.length; row++) {
        d = {};
        for (h = 0; h < headers.length; h++) {
            d[headers[h]] = data[row][h];
        }
        parsed.push(d);
    }

    document.getElementById("id_data-json").value = JSON.stringify({'metadata': metadata_values, 'data': parsed});
};

$("#template-save").click(function() {
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
});

$("#var-save").click(function() {
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
});


hot = new Handsontable(container, {
data: [['']],
rowHeaders: true,
colHeaders: get_template(),
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

document.getElementById('add-row').onclick = function() {
hot.alter('insert_row', 1);
};

document.getElementById('template-select').onchange = function() {
    get_template($(this).val());
};



