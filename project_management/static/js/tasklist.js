var p_id = window.p_id;
var Backbone = window.Backbone;
var _ = window._;
var $ = window.$;
var tasks;
var taskDetail;



var TaskModel = Backbone.Model.extend({
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
    className: 'list-group-item task-item',
    events: {
        'click': 'clickAction',
    },
    initialize: function(){
        this.render();
    },
    render: function(){
        this.$el.html(this.model.get('name'));
        return this;
    },
    clickAction: function(){
        taskDetail = new TaskDetailView({model: this.model});
    }
});


var TaskListView = Backbone.View.extend({
    el: '#task-list',
    initialize: function(){
        this.listenTo(this.collection, 'sync', this.viewSync);
        this.listenTo(this.collection, 'change', this.viewSync);
        this.render();
    },
    render: function(){
        var self = this;
        this.collection.each(function(task){
            self.$el.append(new TaskView({model: task}).el);

        });

        return this;
    },
    viewSync: function(){
        this.$el.empty();
        this.render();
    },
});

// View that displays changes content of a modal
var TaskDetailView = Backbone.View.extend({
    el: '#taskModal',
    template: _.template($('#modalTemplate').html()),
    events: {
        'click #save-btn': 'saveTask'
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
        this.model.save();
        this.$el.modal('hide');
        this.destroy();
    }

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


});


