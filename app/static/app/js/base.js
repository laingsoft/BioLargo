$(document).ready(function() {
    var svginjection = document.querySelectorAll('img.iconic-sprite');
    SVGInjector(svginjection);

    // From https://docs.djangoproject.com/en/1.11/ref/csrf/
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

    $(".notif_dismiss").click(function(){
        id = $(this).data("id");

        var notif_divs = $(".notif"+String(id)).parent();

        $(".notif"+String(id)).remove();
        $("#notif-count").text($("#notif-count").text() - 1);

        if (notif_divs[0].childElementCount == 0){
            empty = document.createElement("li");
            empty.className = "list-group-item";
            text = document.createTextNode("No new notifications");
            empty.appendChild(text);

            $(notif_divs).append(empty);
        }

        $.post('/app/notif_read/', {'pk': id});
    });
});
