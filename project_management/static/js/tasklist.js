function check_handler(e) {
    if ($(this).is(":checked")) {
        val = prompt('Enter project id');
        if (!val) {
            $(this).prop('checked', false);
        };
    }
    e.stopPropagation();
};

function task_click_handler(e) {
    $('#task-modal').modal('toggle');
};

$('#new_task').submit(function(e) {
    var form = $(this);

    $.post(form.attr('action'), form.serialize(), function() {
        $.get(form.attr('action'), function(tasks) {
            var ul = $('#incomplete');
            ul.empty();
            ids = Object.keys(tasks)
            for (i = 0; i < ids.length; i++) {
                li = document.createElement('li');
                li.id = ids[i];
                li.className = 'list-group-item task-item'
                checkbox = document.createElement('input');
                checkbox.type = 'checkbox';
                task = document.createTextNode(tasks[ids[i]]);
                li.append(checkbox);
                li.append(task);
                ul.append(li);

                $('.task-item').click(task_click_handler);
                $('input:checkbox').click(check_handler);
            }
        });

        form.trigger("reset");
        $('#task-modal').modal('toggle');
    }).fail(function() {
        console.log("Error");
    });

    e.preventDefault();
    return false;
});

$('.task-item').click(task_click_handler);

$('input:checkbox').click(check_handler);
