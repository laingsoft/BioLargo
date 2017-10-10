function get_columns(){

}

function allowDrop(ev) {
    ev.preventDefault();
}

function drag(ev) {
    console.log(ev)
    ev.dataTransfer.setData("text", ev.target.id);
}

function drop(ev) {
    var data = ev.dataTransfer.getData("text");
    console.log(data)
    ev.target.appendChild(document.getElementById(data))
    ev.preventDefault();
    
}

$(document).ready(function(){
    //TODO: Choose Experiment Set
    //TODO: Initialize the Toolbox with Various types of Graphs
    //TODO: Initialize the X and Y axis with potential columns
    //TODO: Download Session
    //TODO: Restore Session from file




})
