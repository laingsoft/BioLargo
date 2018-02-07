var p_id = window.p_id;
var Backbone = window.Backbone;
var _ = window._;
var $ = window.$;
var tasks;
var taskDetail;

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
    }
});

var TaskCollection = Backbone.Collection.extend({
    url: '/management/projects/' + p_id + '/tasks',
    model: TaskModel,
    parse: function(data){
        return data.data;
    }
});

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


var TaskListView = Backbone.View.extend({
    el: '#task-lists',
    initialize: function(){
        this.listenTo(this.collection, 'sync, add', this.viewSync);
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
});

// View that displays changes content of a modal
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
    }
});

var TaskProgressView = Backbone.View.extend({
    el: '#progress',

});

$(document).ready(function(){
    tasks = new TaskCollection();
    var tasklist = new TaskListView({collection: tasks});

    tasks.fetch();

    $('#addTask').click(function(e){
        taskDetail = new TaskDetailView({model: new TaskModel({name: 'New Task'})});
    });

    $('#taskModal').on('hidden.bs.modal', function(e){
        taskDetail.destroy();
    });

    $('#calendar').fullCalendar({
        dayClick: function(date) {
            taskDetail = new TaskDetailView({model: new TaskModel({name: "New Task", due_date: date.format()})});
        },
    });

});
