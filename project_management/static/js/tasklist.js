var p_id = window.p_id;
var Backbone = window.Backbone;
var _ = window._;
var $ = window.$;
var tasks;
var taskDetail;


/**
* Backbone Model for tasks. the fields that are objects are parsed by server.
*/
var UserTaskModel = TaskModel.extend({
    urlRoot: '/app/task_complete/',
});

/**
* Backbone collection for tasks.
*/
var UserTaskCollection = TaskCollection.extend({
    url: '/app/task_complete/',
    model: TaskModel,
});


var UserTaskListView = TaskListView.extend({
    initialize: function() {
        this.listenTo(this.collection, 'sync', this.viewSync);
        this.listenTo(this.collection, 'change', this.viewSync);
        this.viewSync();
    },
})

/*
* The view for the task calendar.
**/
var CalendarView = Backbone.View.extend({
    el: '#calendar',
    initialize: function() {
        this.render();
    },
    render: function() {
        var self = this;

        this.$el.fullCalendar({
            events: function(start, end, timezone, callback) {
                var events = self.collection.to_events();
                callback(events);
            },
            eventClick: function(calEvent) {
                taskDetail = new TaskModalView({ model: self.collection.get(calEvent.id)});
            },
        });
    },
});

var TaskModalView = Backbone.View.extend({
    el: '#taskModal',
    template: _.template($('#modalTemplate').html()),
    events: {
        'change #status': 'changeStatus'
    },
    initialize: function() {
        this.render();
    },
    render: function() {
        this.$el.empty();
        this.$el.html(this.template(this.model.toJSON()));
        this.$el.modal('show');
        return this;
    },

    // clears modal container and removes all listeners.
    destroy: function() {
        this.undelegateEvents();
        this.$el.removeData();
        this.$el.empty();
    },
    changeStatus: function(e) {
        this.model.set('status', this.$('#status').val())
        this.model.save()
    }
});


$(document).ready(function(){
    tasks = new UserTaskCollection();
    tasks.add(tasks_array);
    new UserTaskListView({collection: tasks});
    new CalendarView({collection: tasks}).render();

    $('#addTask').click(function(){
        taskDetail = new TaskModalView({model: new UserTaskModel({name: 'New Task'})});
    });

    $('#taskModal').on('hidden.bs.modal', function(){
        taskDetail.destroy();
    });

});

