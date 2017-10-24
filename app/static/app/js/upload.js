$("input[type=radio]").change(function(){
    url = $(this).val()
    $("#exp-form").attr("action", url);
    $.get(url, {}, function(result){
        form = $("#form");
        form.removeAttr("hidden");
        form.html(result);
        })
});

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
    
