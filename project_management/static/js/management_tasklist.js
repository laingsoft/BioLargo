var p_id = window.p_id;
var Backbone = window.Backbone;
var _ = window._;
var $ = window.$;
var tasks;
var taskDetail;

var ManagementTaskModel = TaskModel.extend({
    urlRoot: '/management/projects/' + p_id + '/tasks'
});

var ManagementTaskCollection = TaskCollection.extend({
    url: '/management/projects/' + p_id + '/tasks'
});

var ManagementTaskListView = TaskListView.extend({
    initialize: function() {
        this.listenTo(this.collection, 'reset, sync', this.viewSync);
        this.listenTo(this.collection, 'add', this.addTask);
        this.listenTo(this.collection, 'change:complete, remove', this.viewSync);
        this.render();
    },
    addTask: function(model) {
        this.$('#todo-list').append(new TaskView({ model: model }));
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
        'click #delete-btn': 'deleteTask',
        'click #complete-btn': 'markComplete',
        'click #in-progress-btn': 'markInProgress',
    },
    initialize: function() {
        this.render();
    },
    render: function() {
        data = this.model.toJSON();

        this.$el.empty();
        this.$el.html(this.template(data));
        var self = this;

        $('#taskAssign').selectize({
            maxItems: 1,
            valueField: 'id',
            labelField: 'name',
            preload: 'focus',
            load: function(q, callback) {
                $.get('/management/projects/find_user/', { 'q': q }, function(res) {
                    callback(res.users);
                })
            },
            onInitialize: function() {
                assigned = self.model.get('assigned');
                var me = this;
                if (assigned) {
                    $.get('/management/projects/find_user/', { 'id': assigned }, function(res) {
                        me.addOption(res);
                        me.setValue(assigned);
                    })
                }
            },
            render: {
                option: function(item, escape) {
                    return '<div>'+escape(item.name)+ ' - ' +  escape(item.email) + '</div>'

                }
            }
        });

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

    // used to delete tasks. hide + deletes modal view afterwards.
    deleteTask: function() {
        var conf = confirm('Are you sure you want to delete task?');
        if (conf) {
            this.model.destroy({ wait: true });
            this.$el.modal('hide');
        }
    },
    markComplete: function() {
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
                taskDetail = new TaskModalView({ model: self.collection.get(calEvent.id) });
            },
            dayClick: function(date) {
                taskDetail = new TaskModalView({
                    model: new ManagementTaskModel({ name: 'New Task', due_date: date.format() })
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


$(document).ready(function() {
    tasks = new ManagementTaskCollection();
    new TaskListView({ collection: tasks });
    new CalendarView({ collection: tasks }).render();

    tasks.fetch({ reset: true });

    $('#addTask').click(function() {
        taskDetail = new TaskModalView({ model: new ManagementTaskModel({ name: 'New Task' }) });
    });

    $('#taskModal').on('hidden.bs.modal', function() {
        taskDetail.destroy();
    });

});