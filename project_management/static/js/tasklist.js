var p_id = window.p_id;
var Backbone = window.Backbone;
var _ = window._;
var $ = window.$;
var tasks;
var taskDetail;



/**
* Backbone Model for tasks. the fields that are objects are parsed by server.
*/
var TaskModel = Backbone.Model.extend({
    urlRoot: '/app/task_complete/',
    defaults: {
        id: null, // id from server
        name: null,
        description: null,
        assigned: null, // this is an objects. has attributes name, email, id
        due_date: null,
        timestamp: null,
        complete: null, // true or false
        related_experiment: null, // object with attributes id and name
    },
    to_event: function(){
        var e = {
            id: this.get('id'),
            title: this.get('name'),
            start: this.get('due_date'),
            color: (this.get('complete')) ? '#ccc' : ''
        };
        return e;
    },
});

/**
* Backbone collection for tasks.
*/
var TaskCollection = Backbone.Collection.extend({
    url: '/management/projects/' + p_id + '/tasks',
    model: TaskModel,
    initialize: function() {
        _.bindAll(this, 'to_events');
    },
    parse: function(data){
        return data.data;
    },
    to_events: function() {
        var e = [];
        this.each(function(task) {
            if (task.get('due_date')){
                e.push(task.to_event());
            }
        });
        return e;
    }
});


/**
* View for individual tasks in the list
*/
var TaskView = Backbone.View.extend({
    tagName: 'li',
    className: 'list-group-item',
    template: _.template($('#taskTemplate').html()),
    events: {
        'click': 'clickAction',
    },
    initialize: function(){
        this.listenTo(this.model, 'sync', this.render);
        this.render();
    },
    render: function(){
        this.$el.html(this.template(this.model.toJSON()));
        var self = this;
        if (this.model.get('complete')) {
            self.$('input:checkbox').attr('checked', true);
        }

        return this;
    },
    clickAction: function(){
        taskDetail = new TaskModalView({model: this.model});
    },
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
    tasks = new TaskCollection();
    tasks.add(tasks_array);
    new TaskListView({collection: tasks});
    new CalendarView({collection: tasks}).render();

    $('#addTask').click(function(){
        taskDetail = new TaskModalView({model: new TaskModel({name: 'New Task'})});
    });

    $('#taskModal').on('hidden.bs.modal', function(){
        taskDetail.destroy();
    });

});
