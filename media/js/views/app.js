define([
		'jquery',
		'underscore',
		'backbone',
		'models/entry',
		'collections/antisocial',
], function($, _, Backbone, Entry, EntryList){
		var EntryView = Backbone.View.extend({
				tagName: 'div',
				template: _.template($('#entry-template').html()),
				initialize: function () {
						this.model.bind('change', this.render, this);
						this.model.bind('remove', this.remove, this);
				},
        remove: function() {
						$(this.el).remove();
				},
				render: function () {
						this.$el.html(this.template(this.model.toJSON()));
						return this;
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
						if (this.idx == 0) {
								// can't go up
								return;
						}
						Entries.at(this.idx).set("current", false);
						this.idx--;
						var e = Entries.at(this.idx);
						e.set("current", true);
						$('html, body').animate({
								scrollTop: $("#ue-" + e.get('id')).offset().top - 50
						}, 500);
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
						if (this.idx > Entries.length - 10) {
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
