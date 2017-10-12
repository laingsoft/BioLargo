function get_columns(){

}
function recv_socket(e){
    console.log("Recieved: "+ e.data);
    columns = JSON.parse(e.data);
    console.log(columns);
    clear_axis();
    for (var i = 0; i< columns.length; i++){
        $("#yaxis").append("<li><span class = 'badge badge-secondary'>"+columns[i]+"<span class='ml-2'><input type='checkbox'></span></span></li>");
        $("#ax").append("<li class = 'list-inline-item'><span class = 'badge badge-secondary'>"+columns[i]+"<span class='ml-2'><input type='checkbox'></span></span></li>");
    }
    

}

function clear_axis(){
    $("#yaxis").empty();
    $("#ax").empty();

}

function fireWebsocket(){
    var divs = document.querySelectorAll("#experiment_selector > div");
    var tagsgroups = []
    for (var i =0; i< divs.length; i++){
        var item = {'id':divs[i].id,'table':divs[i].className.split(' ')[1]};
        tagsgroups.push(item);
    }
    socket.send(JSON.stringify(Object.assign({},tagsgroups)));


}

function allowDrop(ev) {
    ev.preventDefault();
}

function drag(ev) {
    ev.dataTransfer.setData("text", ev.target.id);
}

function drop(ev, el) {
    ev.preventDefault()
    var data = ev.dataTransfer.getData("text");
    el.appendChild(document.getElementById(data))
    fireWebsocket()
}

//Filters the tags by Id. So they are searchable. 
$('#tagFilter').on('change keyup paste',function(){
    var value = $('#tagFilter').val();
    if (value == ''){
        $('.tag').show();
        $('.group').show();
    }else{
        $('.tag').hide();
        $('.group').hide();
    }
    $('div[id*="'+value+'" i]').show();
    
})

$(document).ready(function(){
    //TODO: Choose Experiment Set
    //TODO: Initialize the Toolbox with Various types of Graphs
    //TODO: Initialize the X and Y axis with potential columns
    //TODO: Download Session
    //TODO: Restore Session from file
    socket = new WebSocket("ws://"+ window.location.host);
    socket.onmessage = function(e){
        recv_socket(e);
    }


})

