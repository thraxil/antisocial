var path = require("path")
var webpack = require('webpack')

module.exports = {
    context: __dirname,

    entry: {
        main: './media/js/main',
    },

    output: {
        path: path.resolve('./media/js/dist/'),
        sourceMapFilename: "main.map",
        filename: "main.js",
    },
    
    module: {
        loaders: [
        ],
    },

    resolve: {
        modulesDirectories: ['node_modules', 'media/js'],
        extensions: ['', '.js']
    },
}
