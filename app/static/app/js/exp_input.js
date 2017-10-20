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


function get_template(template_name) {
    $.get("/app/get_template", {
        template: template_name
    }, function(response){
        
        });
}




$(document).ready(function(){

    csrftoken = getCookie('csrftoken');
    $.ajaxSetup({
    beforeSend: function(xhr, settings) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    });
    


    //~ $("input[type=radio]").change(function(){
        //~ var current = $("#form > .upload_fields");
        //~ $("#form").append($("#hidden_fields > .upload_fields"));
        //~ $("#hidden_fields").append(current);
    //~ });
    
    //~ Autocomplete/tagging initalization
    $('#id_tags-group').selectize({
        preload: true,
        plugins: ["restore_on_backspace"],
        placeholder: 'Enter Experiment Group',
        create: true,
        createOnBlur: true,
        maxItems: 1,
        persist: false
    });
    
    $('#id_tags-tags').selectize({
        preload: true,
        placeholder: 'Enter Tags',
        plugins: ['remove_button', "restore_on_backspace" ],
        delimiter: ',',
        create: true,
        createOnBlur: true,
        persist: false,
        hideSelected: true
        });
    
    $('#var-name').selectize({
        valueField: 'value',
        labelField: 'key',
        searchField: 'value',
        plugins: ["restore_on_backspace"],
        placeholder: 'Enter variable name',
        create: true,
        createOnBlur: true,
        maxItems: 1,
        persist: false,
        options: [],
        load: function(query, callback) {
            if (!query.length) return callback();
            $.ajax({
            url: '/app/fields-autocomplete',
            type: 'GET',
            dataType: 'json',
            data: {
                q: query
            },
            error: function() {
                callback();
            },
            success: function(res) {
                callback(res.data);
            }
        });
            
        }
    });
})

