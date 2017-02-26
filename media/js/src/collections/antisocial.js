define([
    'jquery',
    'underscore',
    'backbone',
    'models/entry'
], function($, _, Backbone, Entry) {
    var Entries = Backbone.Collection.extend({
        model: Entry,
        initialize: function() {
            console.log('Entries.initialize()');
        },
        url: function() {
            return '/api/entries/';
        }
    });

    return Entries;
});
