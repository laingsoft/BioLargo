$(document).ready(function(){
    $(".inventory-list-item").click(function(){
	console.log(this)
	// update the Information area of the page
	$("#product-headsup-details > #name").text(this.children.name.textContent);
	$("#product-headsup-details > #description").text(this.children.description.textContent);
	$("#product-headsup-details > #on-hand").text("Quantity On Hand: "+ this.children.onhand.textContent);

	//update the statistics portion of the page
	//todo

	//Get the info from the associated attrs that are related to the inventory item.
	
    });



});
