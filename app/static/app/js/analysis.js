function get_columns(){

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
   



})

