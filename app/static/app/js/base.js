$(function() {
    var svginjection = document.querySelectorAll('img.iconic-sprite');
    SVGInjector(svginjection);
    
    var url = window.location.href;
    
    $(".nav-link").each(function(){
        if (url == (this.href)){
            $(this).addClass("active");
        }
    });
});

function doneLoad(){
    $("#loader").hide();
    $("#content").slideDown();
}
