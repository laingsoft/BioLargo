$("#id_fields").selectize({
        plugins: ['drag_drop', 'remove_button'],
        persist: true,
        create: function(input, callback){
            csrftoken = $('input[name="csrfmiddlewaretoken"]').val();
            $.ajax({
                url: "/admin/app/template/add_field/",
                type: "post",
                data: {
                    field: input
                },
                headers: {
                    'X-CSRFToken': csrftoken
                },
                success: function(data){
                    return callback(data);
                }
            });
        },
        selectOnTab: true,
});