$(document).ready(function(){
    $(".inventory-list-item").click(function(){
	//console.log(this.children)
	$("#product-headsup-details > #name").text(this.children.name.textContent);
	$("#product-headsup-details > #description").text(this.children.description.textContent);

    });



});
