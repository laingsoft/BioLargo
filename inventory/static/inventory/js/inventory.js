function searchInventory() {
    var input, filter, table, rd, td, i;
    input = document.getElementById("inventory-search");
    filter = input.value.toUpperCase();
    table = document.getElementById("inventory-table");
    tr = table.getElementsByTagName("tr");
    for (i=0; i< tr.length; i++){
	console.log(tr[i]);
	td = tr[i].getElementsByTagName("td")[0];
	if (td){
	    if (td.innerHTML.toUpperCase().indexOf(filter) > -1){
		tr[i].style.display = "";
	    } else {
		tr [i].style.display = "none";
	    }
	}
    }
    

}



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
