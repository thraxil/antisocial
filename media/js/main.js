// Require.js allows us to configure shortcut alias
// Their usage will become more apparent futher along in the tutorial.

var $ = require('jquery');
var Entry = require('./models/entry');
var EntryList = require('./collections/antisocial');
var AppView = require('./views/app');

var app = new AppView();
console.log(app);
console.log('made new app');
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
