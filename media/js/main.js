// Require.js allows us to configure shortcut alias
// Their usage will become more apparent futher along in the tutorial.
require.config({
  paths: {
    // Major libraries
    jquery: 'libs/jquery/jquery-min',
    underscore: 'libs/underscore/underscore-min',
    backbone: 'libs/backbone/backbone-min',

    // Require.js plugins
    text: 'libs/require/text',
    order: 'libs/require/order'
  },
	urlArgs: "bust=" +  (new Date()).getTime()

});

// Let's kick off the application

require([
		'jquery',
		'models/entry',
		'collections/antisocial',
		'views/app'
], function($, Entry, EntryList, AppView){
		var app = new AppView;
		console.log(app);
		console.log("made new app");
		$("body").keyup(function() {
				var c = String.fromCharCode(event.keyCode);
				if (c == 'J') {
						app.next();
				}
				if (c == 'K') {
						app.prev();
				}
				if (c == 'R') {
						app.reload();
				};
		});
});
