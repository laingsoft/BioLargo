var p_id = window.p_id;
var Backbone = window.Backbone;
var _ = window._;
var $ = window.$;
var tasks;
var taskDetail;

/**
* Backbone Model for tasks.
*/
var TaskModel = Backbone.Model.extend({
    urlRoot: '/management/projects/' + p_id + '/tasks',
    defaults: {
        id: null,
        name: null,
        description: null,
        assigned: null,
        due_date: null,
        timestamp: null,
        complete: null
    },
    to_event: function(){
        var e = {
            id: this.get('id'),
            title: this.get('name'),
            start: this.get('due_date')
        };
        return e;
    },
    validate: function(attrs) {
        if (attrs.name.length < 1){
            return 'Task name is required.';
        }

        if (attrs.description.length < 1){
            return 'A description is required.';
        }

        if (new Date(attrs.due_date) < new Date()){
            return 'Due date is in the past.';
        }
    }
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
        'click :checkbox': 'check'
    },
    initialize: function(){
        this.listenTo(this.model, 'remove', this.remove);
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
    check: function(e){
        this.model.set('complete', this.$('input:checkbox').is(':checked'));
        this.model.save();
        e.stopPropagation();
    }
});

/**
* View for rendering a list of tasks
*/
var TaskListView = Backbone.View.extend({
    el: '#task-lists',
    initialize: function(){
        this.listenTo(this.collection, 'reset, sync', this.viewSync);
        this.listenTo(this.collection, 'add', this.addTask);
        this.listenTo(this.collection, 'change:complete, remove', this.viewSync);
        this.render();
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
* View for the modal for updating and editing tasks. Used for just details as
* well
*/
var TaskModalView = Backbone.View.extend({
    el: '#taskModal',
    template: _.template($('#modalTemplate').html()),
    events: {
        'click #save-btn': 'saveTask',
        'click #delete-btn': 'deleteTask'
    },
    initialize: function(){
        this.render();
    },
    render: function(){
        this.$el.empty();
        this.$el.html(this.template(this.model.toJSON()));
        this.$el.modal('show');
        // $('#taskAssign').selectize();
        return this;
    },

    // clears modal container and removes all listeners.
    destroy: function(){
        this.undelegateEvents();
        this.$el.removeData();
        this.$el.empty();
    },

    //  called when save button is clicked.
    //  validates data before saving to model and server.
    //  state of edited objects should persist as long as it is valid.
    saveTask: function(){
        var self = this;
        var values = {};
        $('#taskForm :input').each(function() {
            values[this.name] = this.value;
        });

        self.model.set(values, {validate: true});

        if (this.model.isValid()){
            this.model.save(null, {
                wait: true,
                success: function(model, response){
                    self.model.set('id', response.data.id);
                    tasks.add(self.model);
                },
                error: function(response) {
                    console.log(response);
                }
            });

            this.$el.modal('hide');
        }
    },

    // used to delete tasks. hide + deletes modal view afterwards.
    deleteTask: function(){
        var conf = confirm('Are you sure you want to delete task?');
        if (conf){
            this.model.destroy({wait: true});
            this.$el.modal('hide');
        }
    },
});

/*
The view for the calendar. Works with some weirdness.
**/
var CalendarView = Backbone.View.extend({
    el: '#calendar',
    initialize: function() {
        _.bindAll(this, 'addAll');
        this.listenToOnce(this.collection, 'reset', this.addAll);
        this.listenTo(this.collection, 'add', this.rerender);
        this.listenTo(this.collection, 'change', this.rerender);
        this.listenTo(this.collection, 'remove', this.rerender);
    },
    render: function() {
        var self = this;

        this.$el.fullCalendar({
            editable: true,
            eventClick: function(calEvent) {
                taskDetail = new TaskModalView({ model: self.collection.get(calEvent.id)});
            },
            dayClick: function(date) {
                taskDetail = new TaskModalView({model: new TaskModel({name: 'New Task', due_date: date.format()})
                });
            },
            eventDrop: function(calEvent) {
                var task = self.collection.get(calEvent.id);
                task.set('due_date', calEvent.start.format());
                task.save();
            }
        });
    },
    //  method called when the first collection fetch is called. Used to
    // populate the calendar events.
    addAll: function() {
        var self = this;
        this.$el.fullCalendar('addEventSource', function(start, end, timezone, callback) {
            var events = self.collection.to_events();
            callback(events);

        });
        this.$el.fullCalendar('rerenderEvents');
    },

    // called on update, add, delete. Re-renders events after a change in the
    // collection.
    rerender: function() {
        this.$el.fullCalendar('refetchEvents');
    }
});


$(document).ready(function(){
    tasks = new TaskCollection();
    new TaskListView({collection: tasks});
    new CalendarView({collection: tasks}).render();

    tasks.fetch({reset: true});

    $('#addTask').click(function(){
        taskDetail = new TaskModalView({model: new TaskModel({name: 'New Task'})});
    });

    $('#taskModal').on('hidden.bs.modal', function(){
        taskDetail.destroy();
    });

});
