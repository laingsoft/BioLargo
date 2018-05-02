var navlist = {"/": "home-nav",
	       "/features/": "features-nav",
	       "/contactus/": "contact-nav" }

$(document).ready(function() {
    $("#"+navlist[window.location.pathname]).addClass("active");
});
