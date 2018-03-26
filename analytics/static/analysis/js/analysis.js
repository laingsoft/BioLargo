var container = $('#container')

function dragStartHandler(evt) {
    evt.dataTransfer.effectAllowed = 'move';
    evt.dataTransfer.setData('text/plain', evt.target.dataset.toolName);
    return true;
}

function dragEnterHandler(evt) {
    evt.preventDefault();
    evt.stopPropagation();
}

function dragOverHandler(evt) {
    evt.preventDefault();
}

function dropHandler(evt) {
    evt.preventDefault();
    var toolName = evt.dataTransfer.getData('text/plain');
    container.append(`
    <div class="row">
    <div class="col">
        <div class="card">
            <div class="card-body">
                <div class="card-block">
                    <h5 class="card-title">${toolName}</h5>
                </div>
            </div>
        </div>
    </div>
</div>
        `)

}

$(document).ready(function(){
    var tools = document.querySelectorAll('.tool-list .list-group-item');

    [].forEach.call(tools, function(tool){
        tool.addEventListener('dragstart', dragStartHandler, false);
    })

    var drop_target = document.querySelector(".main")


    drop_target.addEventListener('dragenter', dragEnterHandler)
    drop_target.addEventListener('dragover', dragOverHandler)
    drop_target.addEventListener('drop', dropHandler)

})
