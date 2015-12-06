NODE_MODULES=./node_modules
JS_SENTINAL=$(NODE_MODULES)/sentinal
JSHINT=$(NODE_MODULES)/jshint/bin/jshint
JSCS=$(NODE_MODULES)/jscs/bin/jscs
WEBPACK=$(NODE_MODULES)/.bin/webpack
WEBPACK_CONFIG=webpack.config.js

jshint: $(JS_SENTINAL)
	$(JSHINT) $(JS_FILES)

jscs: $(JS_SENTINAL)
	$(JSCS) $(JS_FILES)

$(JS_SENTINAL): package.json
	rm -rf $(NODE_MODULES)
	npm install
	touch $(JS_SENTINAL)

media/js/dist/main.js: $(JS_SENTINAL) $(JS_FILES) webpack.*.config.js
	$(WEBPACK) --config $(WEBPACK_CONFIG)

webpack:
	make media/js/dist/main.js
