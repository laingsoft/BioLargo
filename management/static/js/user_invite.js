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


$("#invite").click(function(){
    $. ajax({
        type: 'GET',
        url: "/accounts/invite/",
        dataType: 'json',
        success: function(data) {
            //console.log(data.token);
            $("#inviteLink").val(
                "http://"+
                    window.location.host + "/" +
                    "accounts/invite/"+
                    data.token);
            $("#inviteLink").show()
        }
    })
});
