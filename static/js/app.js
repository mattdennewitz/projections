var PlayerOverview = Backbone.Model.extend({});


var PlayerOverviews = Backbone.Collection.extend({
    model: PlayerOverview,
    req: null,

    initialize: function() {
        _.bindAll(this, 'load');
    },

    load: function() {
        var self = this;

        this.req = $.ajax({
            url: '/api/players/',
            data: {},
        }).done(function(objs) {
            self.reset(objs)
        });
    }
});


var PlayerRow = Backbone.View.extend({
    events: {
        'click .kept-toggle': 'on_toggle'
    },

    templates: {
        kept: _.template('<input class="kept-toggle" type="checkbox" <%= checked %> data-playerid="<%= playerid %>" />'),
        row: _.template(
            '<tr>' +
            '  <td><%= name %></td>' +
            '  <td><%= pos %></td>' +
            '  <td><%= fval %></td>' +
            '</tr>'
        )
    },

    initialize: function(opts) {
        _.bindAll(this, 'render', 'on_toggle');
        this.model = opts.model;
        this.parent = opts.parent;

        this.render();
    },

    on_toggle: function() {
        var value = this.$('.kept-toggle').prop('checked');

        this.model.set('is_kept', value);

        if(value === true)
            this.$el.addClass('kept');
        else
            this.$el.removeClass('kept');
    },

    render: function() {
        var $el = $(this.templates.row(this.model.attributes));

        /* add "kept" toggle */
        var $toggle = $(this.templates.kept({
            checked: (this.model.get('is_kept') === true) ? 'checked' : '',
            playerid: this.model.get('playerid')
        }));

        $el.append( $('<td></td>').append($toggle) );

        /* indicate at row level if player is kept */
        if(this.model.get('is_kept') === true)
            $el.addClass('kept');

        this.setElement($el);

        return this.$el;
    }
});


var PlayerTable = Backbone.View.extend({
    collection: new PlayerOverviews,

    initialize: function() {
        _.bindAll(this, 'filter_view', 'render');

        this.collection.on('reset add remove', this.render);
        this.collection.load();
    },

    /* passes a filtered subset of the collection
       to render, renders. */
    filter_view: function(params) {
        this.render(this.collection.where(params));
    },

    render: function(objs) {
        var self = this;

        if(!(objs instanceof Array))
            objs = objs.toArray() || this.collection.toArray();

        this.$('tbody').remove();

        var $tbody = $('<tbody></tbody>');

        console.log('start');

        var rows = [];

        _(objs).each(function(obj) {
            rows.push(new PlayerRow({
                model: obj
            }).render());
        });

        $tbody.append(rows);
        this.$el.append($tbody);

        console.log('stop');
    }
});


var ControlPanel = Backbone.View.extend({
    events: {
        'click #unkept-only': 'unkept_only'
    },

    initialize: function(opts) {
        _.bindAll(this, 'unkept_only');

        this.app = opts.app;
    },

    unkept_only: function() {
        var filter = {};

        if(this.$('#unkept-only').prop('checked'))
            filter = {is_kept: false};
            
        this.app.filter_view(filter);
    }
});


$(function() {
    window.app = new PlayerTable({el: $('table')});
    window.controls = new ControlPanel({
        el: $('#controls'),
        app: window.app
    });
});
