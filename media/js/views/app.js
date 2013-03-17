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
						this.model.bind('destroy', this.remove, this);
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
						Entries.bind('add',   this.addOne, this);
						Entries.bind('reset', this.addAll, this);
						Entries.bind('all',   this.render, this);
						Entries.fetch();
				},
				render: function () {
						return this;
				},
				addOne: function(entry) {
						var view = new EntryView({model: entry});
						this.$el.append(view.render().el);
				},
				addAll: function() {
						Entries.each(this.addOne, this);
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
				}
		});
		return AppView;
});
