$(function() {
    var svginjection = document.querySelectorAll('img.iconic-sprite');
    SVGInjector(svginjection);
    
    var url = window.location.href;
    
    $(".nav-link").each(function(){
        if (url == (this.href)){
            $(this).addClass("active");
        }
    });

    $(".sidebar").mouseenter(function(){
        $('.icon').hide();
        $('.description').show();
    });
    $(".sidebar").mouseleave(function(){
        $('.description').hide();
        $('.icon').slideDown();
    });
});

function doneLoad(){
    $("#loader").hide();
    $("#content").slideDown();
}
