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

$('#id_tags-project').selectize({
    preload: true,
    plugins: ["restore_on_backspace"],
    placeholder: 'Enter Project',
    create: true,
    createOnBlur: true,
    maxItems: 1,
    persist: false
});

$('#id_tags-tags').selectize({
    preload: true,
    placeholder: 'Enter Tags',
    plugins: ['remove_button', "restore_on_backspace"],
    delimiter: ',',
    create: true,
    createOnBlur: true,
    persist: false,
    hideSelected: true
});

$('#id_exp_form-template').selectize({
    preload: true,
    placeholder: 'Select a template',
});
