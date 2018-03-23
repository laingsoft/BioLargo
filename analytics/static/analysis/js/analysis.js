$(document).ready(function(){
    var tools = document.querySelectorAll('.tool-list .list-group-item');

    tools.forEach(function(tool){
        tool.addEventListener('dragstart', function(evt){
            evt.stopPropagation();
            evt.dataTransfer.effectAllowed = 'move';
            evt.dataTransfer.setData('text/plain', '');
        });
    })
})
