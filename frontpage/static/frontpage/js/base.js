var navlist = {"/": "home-nav",
	       "/features/": "features-nav",
	       "/contactus/": "contact-nav" }

$(document).ready(function() {
    $("#"+navlist[window.location.pathname]).addClass("active");
});


function ScrollTo(id){
    $('html,body').animate({
	scrollTop: $("#"+id).offset().top},
			   'slow');

}
    
