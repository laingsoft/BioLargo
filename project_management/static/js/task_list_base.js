var TaskModel = Backbone.Model.extend({
    defaults: {
        id: null,
        name: null,
        description: null,
        assigned: null,
        due_date: null,
        complete: null,
        in_progress: null,
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
    },
});

/**
* Backbone collection for tasks.
*/
var TaskCollection = Backbone.Collection.extend({
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
        this.listenTo(this.model, 'remove', this.remove);
        this.listenTo(this.model, 'sync', this.render);
        this.render();
    },
    render: function(){
        this.$el.html(this.template(this.model.toJSON()));
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
        this.listenTo(this.collection, 'reset, sync', this.viewSync);
    },
    render: function(){
        var self = this;
        this.collection.each(function(task){
            if (task.get('complete')){
                self.$('#completed-list').append(new TaskView({model: task}).el);
            }
            else if (task.get('in_progress')) {
                self.$('#in-progress-list').append(new TaskView({model: task}).el);
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
        if (this.$('#in-progress-list li').length ===  0) {
            self.$('#in-progress-list').append('<li class="list-group-item">No in-progress items found.</li>');
        }

        return this;
    },
    viewSync: function(){
        this.$('#todo-list').empty();
        this.$('#completed-list').empty();
        this.$('#in-progress-list').empty();
        this.render();
    },
});


var TaskModalView = Backbone.View.extend({
    el: '#taskModal',
    template: _.template($('#modalTemplate').html()),
    events: {
        'click #complete-btn': 'markComplete',
        'click #in-progress-btn': 'markInProgress',
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

    //  called when save button is clicked.
    //  validates data before saving to model and server.
    //  state of edited objects should persist as long as it is valid.
    saveTask: function() {
        var self = this;
        var values = {};
        $('#taskForm :input').each(function() {
            values[this.name] = this.value;
        });

        self.model.set(values, { validate: true });

        if (this.model.isValid()) {
            this.model.save(null, {
                wait: true,
                success: function(model, response) {
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

    markComplete: function() {
        new RelatedExperimentView({model: this.model }).render();
        this.model.set({ 'in_progress': false, 'complete': true });
    },
    markInProgress: function() {
        this.model.set({ 'in_progress': true, 'complete': false });
    },
    setStatus: function() {
        this.$('#status');
    },
    markIncomplete: function() {
        this.model.set('complete', false);
    },
});


