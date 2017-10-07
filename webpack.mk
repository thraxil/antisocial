media/dist/app.js: webpack.config.js elm-package.json media/elm/src/*
	./node_modules/.bin/webpack

webpack: media/dist/app.js

webpack-p:
	./node_modules/.bin/webpack -p

.PHONY: webpack webpack-p
