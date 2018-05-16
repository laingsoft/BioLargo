

$(document).ready(function(){
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
		console.log("worked");

            }
        });
    });
});

