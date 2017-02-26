require.config({
    map: {
        '*': {
            'jquery': 'jquery-private'
        },
        'jquery-private': {
            'jquery': 'jquery'
        }
    },
    paths: {
        jquery: '../libs/jquery/jquery-min',
        'jquery-private': '../libs/jquery/jquery-private',

        underscore: '../libs/underscore/underscore-min',
        backbone: '../libs/backbone/backbone-min',
    },
    shim: {
        backbone: {
            'deps': ['underscore', 'jquery'],
            'exports': 'Backbone'
        },
        underscore: {
            'exports': '_'
        }
    },
    urlArgs: 'bust=' +  (new Date()).getTime()
});

require([
    'jquery',

    'models/entry',
    'collections/antisocial',
    'views/app'
], function($, Entry, EntryList, AppView) {

    var app = new AppView();
    $('body').keyup(function() {
        var c = String.fromCharCode(event.keyCode);
        if (c == 'J') {
            app.next();
        }
        if (c == 'K') {
            app.prev();
        }
        if (c == 'R') {
            app.reload();
        }
    });
});
