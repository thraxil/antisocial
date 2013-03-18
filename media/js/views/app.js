define([
		'jquery',
		'underscore',
		'backbone',
		'models/entry',
		'collections/antisocial',
], function($, _, Backbone, Entry, EntryList){
    // if we know that fetching new items from the server won't
    // actually get us any new ones (ie, we're almost at the end)
    // might as well just not do that
    var disableFetch = false;
		var EntryView = Backbone.View.extend({
				tagName: 'div',
				template: _.template($('#entry-template').html()),
				initialize: function () {
						this.model.bind('change', this.render, this);
						this.model.bind('remove', this.remove, this);
						this.model.bind('sync', this.updateCount, this);
				},
        remove: function() {
						$(this.el).remove();
				},
				render: function () {
						this.$el.html(this.template(this.model.toJSON()));
						return this;
				},
				updateCount: function (model, response, options) {
						if (model.get('unread_count')) {
                if (parseInt(model.get('unread_count'), 10) < 10) {
                    disableFetch = true;
                } else {
                    disableFetch = false;
                }
								$("#unread-count-var").html(model.get('unread_count'));
						}
				}
		});

		var Entries = new EntryList;
		var AppView = Backbone.View.extend({
				el: '#entries-container',
				idx: 0,
				initialize: function () {
						this._entryViews = [];
						Entries.bind('add',   this.addOne, this);
						Entries.bind('reset', this.addAll, this);
						Entries.bind('all',   this.render, this);
						Entries.bind('remove', this.remove, this);
						Entries.fetch();
				},
				render: function () {
						return this;
				},
				remove: function(model) {
						var viewToRemove = _(this._entryViews).select(
								function(cv) { return cv.model === model; })[0];
						this._entryViews = _(this._entryViews).without(viewToRemove);
 						$(viewToRemove.el).remove();
				},
				addOne: function(entry) {
						var view = new EntryView({model: entry});
						this._entryViews.push(view);
						this.$el.append(view.render().el);
				},
				addAll: function() {
						Entries.each(this.addOne, this);
				},
				reload: function() {
						Entries.each(this.remove, this);
						Entries.fetch();
						this.idx = 0;
				},
				prev: function() {
						if (this.idx < 2) {
								// can't go up
								return;
						}
						// collapse the one that's open
						Entries.at(this.idx - 1).set("current", false);
						// undo the advance from before
						this.idx--;
						// and again to actually back up to the previous
						this.idx--;
						var e = Entries.at(this.idx);
						e.set("current", true);
						$('html, body').animate({
								scrollTop: $("#ue-" + e.get('id')).offset().top - 50
						}, 500);
						// re-advance so the next 'j' will work as expected
						this.idx++;
				},
				next: function() {
						if (this.idx > 0) {
								Entries.at(this.idx - 1).set("current", false);
						}
						var e = Entries.at(this.idx);
						e.set("current", true);
						this.idx++;
						$('html, body').animate({
								scrollTop: $("#ue-" + e.get('id')).offset().top - 50
						}, 500);
						e.markRead();
						if (!disableFetch && this.idx > Entries.length - 10) {
								var toremove = [];
								for (var i = 0; i < Entries.length; i++) {
										if (i != this.idx - 1) {
												toremove.push(Entries.at(i));
										}
								}
								_(toremove).each(this.remove, this);
								Entries.fetch();
                this.idx = 1;
								// elements on the page move around
								// so get back where we want
								$('html, body').animate({
										scrollTop: $("#ue-" + e.get('id')).offset().top - 50
								}, 100);

						}

				}
		});
		return AppView;
});
