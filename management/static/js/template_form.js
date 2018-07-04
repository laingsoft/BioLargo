function CreateField(input, callback){
    csrftoken = getCookie('csrftoken');
    var data = {"name":input};
    var value;
    $.ajax({
            beforeSend: function(xhr, settings){
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            },
            url: "/api/field/",
            dataType: 'json',
            method: 'POST',
            data: data,
            success: function(data) {
                value = data["id"];              
                callback({value: value, text:input});
                
            }
        });
    
    
};
