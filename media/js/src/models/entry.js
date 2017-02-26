define([
    'jquery',
    'underscore',
    'backbone'
], function($, _, Backbone) {
    var Entry = Backbone.Model.extend({

        defaults: function() {
            return {
                title: 'untitled',
                current: false,
                read: false
            };
        },

        url: function() {
            return '/api/entry/' + this.get('id') + '/';
        },

        initialize: function() {
        },

        toggle: function() {
            this.save();
        },

        markRead: function() {
            this.save({read: true});
        },
    });
    return Entry;
});
