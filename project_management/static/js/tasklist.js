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


/**
* View for rendering a list of tasks
*/
var TaskListView = Backbone.View.extend({
    el: '#task-lists',
    initialize: function(){
        this.listenTo(this.collection, 'change:complete', this.viewSync);
        this.viewSync();
    },
    render: function(){
        var self = this;
        this.collection.each(function(task){
            if (task.get('complete')){
                self.$('#completed-list').append(new TaskView({model: task}).el);
            }
            else {
                self.$('#todo-list').append(new TaskView({model: task}).el);
            }

        });

        if (this.$('#todo-list li').length === 0) {
            self.$('#todo-list').append('<li class="list-group-item">No todo items found.</li>');
        }

        if (this.$('#completed-list li').length ===  0) {
            self.$('#completed-list').append('<li class="list-group-item">No completed items found.</li>');
        }

        return this;
    },
    viewSync: function(){
        this.$('#todo-list').empty();
        this.$('#completed-list').empty();
        this.render();
    },
    addTask : function(model){
        this.$('#todo-list').append(new TaskView({model: model}));
    }
});

/**
* View for the modal to show task details
*/
var TaskModalView = Backbone.View.extend({
    el: '#taskModal',
    template: _.template($('#modalTemplate').html()),
    events: {
        'click #complete-btn': 'markComplete'
    },
    initialize: function(){
        this.render();
    },
    render: function(){
        this.$el.empty();
        this.$el.html(this.template(this.model.toJSON()));
        this.$el.modal('show');
        return this;
    },

    // clears modal container and removes all listeners.
    destroy: function(){
        this.undelegateEvents();
        this.$el.removeData();
        this.$el.empty();
    },
    markComplete: function() {
        new RelatedExperimentView({model: this.model }).render();
    }
});

/**
* View related experiment modal. Is created when a user tries to mark a task
* as complete.
*/
var RelatedExperimentView = Backbone.View.extend({
    el: '#addRelated',
    events: {
        'click #skip': 'completed',
        'click #add': 'addRelated'
    },
    render: function() {
        this.$('#related_form')[0].reset();
        this.$el.modal('show');
    },
    completed: function() {
        this.model.set('complete', true);
        this.model.save();
    },
    addRelated: function() {
        var exp_id = this.$('#relatedExperiment').val();
        console.log(exp_id);
        this.model.set('related_experiment', exp_id);
        this.completed();
    }
});


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


$(document).ready(function(){
    tasks = new UserTaskCollection();
    tasks.add(tasks_array);
    new TaskListView({collection: tasks});
    new CalendarView({collection: tasks}).render();

    $('#addTask').click(function(){
        taskDetail = new TaskModalView({model: new UserTaskModel({name: 'New Task'})});
    });

    $('#taskModal').on('hidden.bs.modal', function(){
        taskDetail.destroy();
    });

});

