function showAlert(){
    var alert  = $("<div id='alert' class='row'><div class='alert alert-success'>Experiment Updated!</div></div>");
    alert.appendTo($("body")[0]);
}

function removeAlert(){
    var alert = $("#alert")
    alert.fadeOut("slow", function(){
	alert.remove();
    });
}

$(document).ready(function(){
    $("#material-selector").selectize()
    $(".underlined-hover").click(function(){
	this.contentEditable = true;
    });

    $("#submitSOP").click(function(){
	var csrftoken = getCookie('csrftoken');
	var name = document.getElementById("sop-name").textContent;
	var description = document.getElementById("sop-description").textContent;
	var procedure = JSON.stringify(quill.getContents());
	var data = {"name":name,
		    "description": description,
		    "procedure": procedure,
		    "id": id
		   };
	console.log(data);
	$.ajax({
            beforeSend: function(xhr, settings){
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            },
            url: "/api/sop/",
            dataType: 'json',
            method: 'POST',
            data: data,
            success: function(data) {
		showAlert();
		setTimeout(removeAlert, 3000);
		
            }
        });
    });
});

