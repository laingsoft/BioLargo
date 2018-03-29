var container = $('#container')

/**
* Drag event handlers
*/

function ToolContainer() {

}

function toolDragStartHandler(evt) {
    evt.dataTransfer.effectAllowed = 'move';
    evt.dataTransfer.setData('text/plain', evt.target.dataset.toolName);
    return true;
}

function toolDragEnterHandler(evt) {
    evt.preventDefault();
    evt.stopPropagation();
}

function toolDragOverHandler(evt) {
    evt.preventDefault();
}

function toolDropHandler(evt) {
    evt.preventDefault();
    var toolName = evt.dataTransfer.getData('text/plain');
    // TODO: make collapse and remove work properly.
    container.append(`
<div class="card">
    <div class="card-header">
        ${toolName}
        <div class="card-actions">
            <a href="#"aria-expanded="true">-</a>
            <a href="#">x</a>
        </div>
    </div>
    <div class="card-body collapse show" id="">
    </div>
</div>
        `)
window.scrollTo(0, document.body.scrollHeight);
}

$(document).ready(function(){
    var tools = document.querySelectorAll('.tool-list .list-group-item');

    [].forEach.call(tools, function(tool){
        tool.addEventListener('dragstart', toolDragStartHandler, false);
    })

    var drop_target = document.querySelector(".main")


    drop_target.addEventListener('dragenter', toolDragEnterHandler)
    drop_target.addEventListener('dragover', toolDragOverHandler)
    drop_target.addEventListener('drop', toolDropHandler)

    socket = new WebSocket("ws://" + window.location.host + '/analytics/');
})
