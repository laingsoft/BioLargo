function get_columns(){

}
function recv_socket(e){
    console.log("Recieved: "+ e.data);
    columns = JSON.parse(e.data);
    console.log(columns);
    clear_axis();
    for (var i = 0; i< columns.length; i++){
       // $("#yaxis").append("<li id='"+columns[i]+"'><span class = 'badge badge-secondary ycol'>"+columns[i]+"<span class='ml-2'><input type='checkbox'></span></span></li>");
        $("#listcol").append("<li id='"+columns[i]+"' class = 'list-inline-item colitem' draggable='true' ondragstart='drag(event)'><span class = 'badge badge-secondary'>"+columns[i]+"</span></li>");
    }
    

}

function clear_axis(){
    $("#listcol").empty();

}

function fireWebsocket(){
    var divs = document.querySelectorAll("#experiment_selector > div");
    var tagsgroups = []
    for (var i =0; i< divs.length; i++){
        var item = {'id':divs[i].id,'table':divs[i].className.split(' ')[1]};
        tagsgroups.push(item);
    }
    socket.send(JSON.stringify({'action':'getcols', 'data':Object.assign({},tagsgroups)}));


}

function allowDrop(ev) {
    ev.preventDefault();
}

function drag(ev) {
    ev.dataTransfer.setData("text", ev.target.id);
}


function drop_tag(ev, el) {
    ev.preventDefault();
    console.log(el.id);
    var data = ev.dataTransfer.getData("text");
    //var nodecopy = document.getElementById(data).cloneNode(true);
    //nodecopy.id = data;
    var originalDiv = document.getElementById(data);
    console.log(originalDiv.className.split(' ')[1]);
    if ((originalDiv.className.split(' ')[1] == 'tag') || (originalDiv.className.split(' ')[1] == 'group')) {
        el.appendChild(originalDiv);
        //el.appendChild(nodecopy);
        fireWebsocket()
    }else{
        return;
    }
}
function drop_axis(ev, el){
    ev.preventDefault();
    var data = ev.dataTransfer.getData("text");
    console.log(data);
    var nodecopy = document.getElementById(data).cloneNode(true);
    nodecopy.id = 'ax_x' + data;
    el.appendChild(nodecopy);
    //firewebsocket;

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
    socket = new WebSocket("ws://"+ window.location.host + window.location.pathname);
    socket.onmessage = function(e){
        recv_socket(e);
    }
    var ctx = document.getElementById("chart").getContext("2d");
    var test = {'type':'line','data':{'datasets':[{
                label: "Test Set 1",
                data: [{
                    x: 1,
                    y: 2,
                }, {
                    x: 2,
                    y: 4,
                }, {
                    x: 3,
                    y: 6,
                }]
    }]}};
    window.scatter = new Chart(ctx, test);
    


})

