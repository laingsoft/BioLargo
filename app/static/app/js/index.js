var search_by = 'ID';

jQuery(document).ready(function($){
	$(".metadatarow").click(function(){
	    window.location = $(this).data("href");
	});
    
    $(".input-group-btn .dropdown-menu li").click(function(){
        search_by = $(this).text();
        $('#search_select').text("Search by " + search_by);
        });
});


