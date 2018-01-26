// From https://stackoverflow.com/a/39525988 2018/01/23
$.fn.extend({
    toggleText: function(a, b) {
        return this.text(this.text() == b ? a : b);
    }
});

//  csrftoken setup from Django documentation.

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

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

var button = $("#watch")

button.click(function() {
    $.post("/app/watch/", {pk: id, type: type }, function(r) {
        if (r.success) {
            button.toggleClass("disabled");
            button.toggleText("Watch", "Unwatch")

        } else {

        }
    })
})
