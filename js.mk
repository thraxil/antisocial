jshint: node_modules/jshint/bin/jshint
	./node_modules/jshint/bin/jshint $(JS_FILES)

jscs: node_modules/jscs/bin/jscs
	./node_modules/jscs/bin/jscs $(JS_FILES)

node_modules/jshint/bin/jshint:
	npm install jshint

node_modules/jscs/bin/jscs:
	npm install jscs
