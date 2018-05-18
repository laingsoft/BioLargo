function searchInventory() {
    var input, filter, table, rd, td, i;
    input = document.getElementById("inventory-search");
    filter = input.value.toUpperCase();
    table = document.getElementById("inventory-table");
    tr = table.getElementsByTagName("tr");
    for (i=0; i< tr.length; i++){
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
    var editToggle = false;
    $(".inventory-list-item").click(function(){
	console.log(this)
	// update the Information area of the page
	$("#product-headsup-details > #name").text(this.children.name.textContent);
	$("#product-headsup-details > #description").text(this.children.description.textContent);
	$("#product-headsup-details > #on-hand").text("Quantity On Hand: "+ this.children.onhand.textContent);
	
	//update the statistics portion of the page
	//todo

	//Get the info from the associated attrs that are related to the inventory item.

	//make it active, and the others non-active
	$(".inventory-list-item").removeClass("active");
	$(this).addClass("active");
	
    });

    $("#inventory-filterby").change(function(){
	var filter = this.value;
	console.log(filter);
	console.log(filter == "All");
	$(".inventory-list-item").hide();
	$("[itemcategory="+filter+"]").show();
	if (filter == "All"){
	    $(".inventory-list-item").show();
	}
    });

    $("#id_category").selectize({
	create:true,
	sortField: 'text'
    });

    $("#item-edit-toggle").click(function(){
	console.log(editToggle);
	if(!editToggle){
	    var editButtons = $("<div></div>");
	    var submit = $("<button>Submit</button>");
	    var cancel = $("<button>Cancel</button>");
	    submit.addClass("btn btn-primary");
	    cancel.addClass("btn btn-cancel");
	    submit.appendTo(editButtons);
	    cancel.appendTo(editButtons);
	    editButtons.addClass("d-flex float-right");
	    editButtons.appendTo("#inventory-item-edit");
	    editToggle = true;
	}else{
	    $("#inventory-item-edit").empty();
	    editToggle = false;
	    
	}
	

    });

});
