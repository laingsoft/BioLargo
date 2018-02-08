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
        return {events: e};
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
        this.listenTo(this.model, 'remove', this.deleteView);
        this.listenTo(this.model, 'change', this.render);
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
        taskDetail = new TaskDetailView({model: this.model});
    },
    deleteView: function(){
        this.undelegateEvents();
        this.$el.removeData().unbind();
        this.remove();
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
        this.listenTo(this.collection, 'change:complete', this.viewSync);
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

        if (this.$('#todo-list li').length == 0) {
            self.$('#todo-list').append('<li class="list-group-item">No todo items found.</li>');
        }

        if (this.$('#completed-list li').length == 0) {
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
* View for the modal for updating and editing tasks
*/
var TaskDetailView = Backbone.View.extend({
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
    destroy: function(){
        this.undelegateEvents();
        this.$el.removeData();
        this.$el.empty();
    },
    saveTask: function(){
        var self = this;
        $('#taskForm :input').each(function(){
            self.model.set(this.name, this.value);
        });

        this.model.save(null, {success: function(model, response){
            self.model.set('id', response.data.id);
        }});

        this.$el.modal('hide');
        tasks.add(this.model);
        this.destroy();
    },
    deleteTask: function(){
        var conf = confirm('Are you sure you want to delete task?');
        if (conf){
            this.model.destroy();
            this.$el.modal('hide');
            this.destroy();
        }
    },
});

var CalendarView = Backbone.View.extend({
    el: '#calendar',
    initialize: function() {
        this.listenTo(this.collection, 'reset', this.addAll);
    },
    render: function() {
        this.$el.fullCalendar({
            editable: true,
        });
    },
    addAll: function() {
        this.$el.fullCalendar('addEventSource', this.collection.to_events());
        this.$el.fullCalendar('rerenderEvents');
    }
});


$(document).ready(function(){
    tasks = new TaskCollection();
    new TaskListView({collection: tasks});
    new CalendarView({collection: tasks}).render();

    tasks.fetch({reset: true});

    $('#addTask').click(function(){
        taskDetail = new TaskDetailView({model: new TaskModel({name: 'New Task'})});
    });

    $('#taskModal').on('hidden.bs.modal', function(){
        taskDetail.destroy();
    });

});
