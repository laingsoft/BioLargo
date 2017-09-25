$(function() {

    var url = window.location.href;

    $(".nav-link").each(function(){
        if (url == (this.href)){
            $(this).addClass("active");
        }
    });
});