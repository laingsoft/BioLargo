var container = document.getElementById('data-table');
var templates;
var data = [[]];
var col;

var groups;

$.getJSON('/app/groups_list', function(data){groups = data.data})


var var_autocomplete;
new autoComplete({
    selector: '#var-name',
    minChars: 1,
    source: function(term, response){
        try { var_autocomplete.abort(); } catch(e){}
        var_autocomplete = $.getJSON('/app/fields-autocomplete', { q: term }, function(data){ response(data.data); });
    }
});

new autoComplete({
    selector: '#id_metadata-group',
    minChars: 0,
    source: function(term, suggest){
        term = term.toLowerCase();
        choices = groups;
        var suggestions = [];
        for (i=0;i<choices.length;i++)
            if (~(choices[i][0]+' '+choices[i][1]).toLowerCase().indexOf(term)) suggestions.push(choices[i]);
        suggest(suggestions);
    },
    renderItem: function (item, search){
        return '<div class="autocomplete-suggestion" data-group-name = "' + item[0]+'" ">'+item[0]+'</div>';

    },
     onSelect: function(e, term, item){
        $('#id_metadata-group').val(item.getAttribute('data-group-name'));
    }
});


var hot = new Handsontable(container, {
    data: data,
    rowHeaders: true,
    colHeaders: true,
    contextMenu: true,
    preventOverflow: 'horizontal',
    manualColumnMove: true,
    manualRowMove: true,
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
