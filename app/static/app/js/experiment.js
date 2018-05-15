// Experiment Javascript
function makeMetadata(data){
    table = $("#metadata-table");
    row = $('<tr></tr>');
    $.each(data, function(key, obj){

        $('<td></td>',{text:key}).appendTo(row);
    })
	row.appendTo(table);
    row = $('<tr></tr>');
    $.each(data, function(key, obj){

        $('<td></td>',{text:obj}).appendTo(row);
    })
	row.appendTo(table);


}
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function deleteExperiment(){
    var csrftoken = getCookie('csrftoken');
    $.ajaxSetup({
        beforeSend: function(xhr, settings){
            if(!this.crossDomain){
                xhr.setRequestHeader('X-CSRFToken', csrftoken);
            }
        }
    });
    $. ajax({
        type: 'POST',
        url: "/app/experimentrm/"+id,
        dataType: 'json',
        success: function(data) {
            // console.log(data);
            if(data.result){
                window.location = '/app/';
            }
        }
    })

}

function makeTable(jsondata){
    table = jQuery("#experimental-data"), row = null, data = null;
    thead = $("#data-table-head");
    //console.log(jsondata);
    //$.each(jsondata, function(key, obj){ $.each(jsondata, function(k, v){ console.log(v)})});
    makeHeaders(jsondata, thead);
    $.each(jsondata, function(key, obj){
        row = $('<tr id='+obj[1]+'></tr>'); // Create a new row
        $.each(obj[0], function(k, v){
            $('<td></td>',{text:v}).appendTo(row);
        });
	row.addClass("table-row-clickable");
	row.append('<td width="5px;"><svg class="icon table-menu" viewBox="0 0 8 8"><use xlink:href="#ellipses"></use></svg></td>');
        row.appendTo(table);
    });

    //add the clickhandler to the rows
    $("#experimental-data tr").click(function(){

	//var form = document.getElementById("annotation-form")
	//if (form != null){
	//    $("#annotation-form").remove();
	//}
	//appendAnnotationForm(this.id);

	});
}

function makeHeaders(jsondata, table){
    //console.log(jsondata);
    row = $('<tr></tr>');
    for (prop in jsondata[0][0]){
        //console.log(prop);
        $('<th></th>',{text:prop}).appendTo(row);
    }
    $('<th> </th>').appendTo(row);
    row.appendTo(table);


}

function ShowImages(imgid){
    var oimage = document.getElementById(imgid);
    var imshow = new Image();
    imshow.src = oimage.src;
    canvas = document.getElementById("removalChart");
    context = canvas.getContext("2d");
    context.drawImage(imshow,0,0, canvas.width, canvas.height);
}


$.ajax({
    url: "/app/experimentjs/"+id,
    dataType: 'json',
    success: function(data) {
	// console.log(data);
        makeTable(data);
        //makeChart(data);
        makeMetadata(metadata);
	ShowImages($(".img_userimg")[0].id);
	$($(".img_userimg")[0]).addClass("active");
	getAnnotations();
    }
});

function commentBuilder(commentObject){
    console.log(commentObject);
    var comment = `<li class = "list-group-item">
        <div class = "media">
        <img src = "https://www.gravatar.com/avatar/e3569fea24b8a64d7b6cf0fd57234ee9?s=40" class="d-flex mr-3">
        <div class = "media-body">
        <h5 class = "mt-0">`+commentObject.user.first_name+`</h5>
        <div class="commentContent">
        <p>`+commentObject.content+`</p>
        </div>
        </div>
        <div class="d-flex justify-content-end">
        <small>`+ new Date(commentObject.timestamp) +`</small>
        </div> 
        </div>
	</li>`;
    $("#commentList").append(comment);


}
function reloadComments(){
    $.ajax({
        method: "GET",
        url: "/api/comment/"+id,
        dataType: 'json',
        data: {},
        success: function(data) {
            $("#commentList").empty();
            //console.log('response')
            //console.log(data);
            for (var key in data){
                commentBuilder(data[key]);
            }
        }
    });
}

function loadAnnotations(data){
    for (var i=0; i< data.length; i++){
	console.log(data[i]);
	//$("#"+data[i].experimentData.id).addClass("annotated");
	$("#"+data[i].experimentData.id).after("<div class='annotation-hidden'>"+data[i].text+"</div><br></br>")
    }
}

function getAnnotations(){
        $.ajax({
        method: "GET",
        url: "/api/annotation/"+id,
        dataType: 'json',
            data: {},
        success: function(data) {
            //loadAnnotations(data);
        }
    });

}


function appendAnnotationForm(id){
    //append the form
    var form ='<tr class="annotation-form" id="annotation-form"><td><label for="annotation">Comment</label><textarea class="form-control" id="annotation" rows="2"></textarea><button class="btn btn-primary submitAnnotation">Submit</button></td></tr>';
    $("#"+id).after(form);

    //add a clickhandler for it

    $(".submitAnnotation").click(function(e){
	var content = $("#annotation");
	var text = content.val();
	var data = {'text':text, 'data_id':id}
	console.log(data);
	$.ajax({
            beforeSend: function(xhr, settings){
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            },
            url: "/api/annotation/",
            dataType: 'json',
            method: 'POST',
            data: data,
            success: function(data) {
		console.log("sent");

            }
        });
    });
    

}

var TABS = {"overviewLink":$("#overview"), "commentLink":$("#commentbox"), "dataLink":$("#data"), "settingsLink":$("#settings")};
$(document).ready(function(){

    $("#removalChart").click(function(){
	var img_selection = $(".img_userimg.active")[0];
	var img = new Image();
	img.src = img_selection.src;
	var canvas = document.getElementById("modalCanvas");
	var context = canvas.getContext("2d");
	canvas.width = img.naturalWidth;
	canvas.height = img.naturalHeight;
	context.drawImage(img, 0, 0);
	$("#img_modal").modal();
    });
    
    $(".img_userimg").click(function(){
	var active = $(".img_userimg.active");
	active.removeClass("active");
	$("#"+this.id).addClass("active");
	ShowImages(this.id);
    });
    


    $("#submitCommentButton").click(function(e){
        var content = $("#newCommentInput");
        content.prop("disabled",true);
        var text = content.val();
        var data = {'content':text, 'exp_id':id};
        //console.log(data);
        $.ajax({
            beforeSend: function(xhr, settings){
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            },
            url: "/api/comment/",
            dataType: 'json',
            method: 'POST',
            data: data,
            success: function(data) {
                content.prop("disabled", false);
                content.val('');
                reloadComments();

            }
        });
    });


	

	



});



