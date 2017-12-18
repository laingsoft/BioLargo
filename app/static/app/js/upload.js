$("document").ready(function(){

    form = $("input[type=radio]:checked").val()
    if (form){
        $("#exp_data").append($("#" + form))
    }

});

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
    hideSelected: true
});

$('#id_exp_form-template').selectize({
    placeholder: 'Select a template',
});
