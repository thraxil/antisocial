var $ = require('jquery');
var _ = require('underscore');
var Backbone = require('backbone');
var Entry = require('models/entry');

var Entries = Backbone.Collection.extend({
    model: Entry,
    initialize: function() {
        console.log('Entries.initialize()');
    },
    url: function() {
        return '/api/entries/';
    }
});

module.exports = Entries;
