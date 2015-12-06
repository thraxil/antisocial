var path = require("path")
var webpack = require('webpack')

module.exports = {
    context: __dirname,

    plugins: [
        new webpack.ProvidePlugin({
            _: "underscore"
        })
    ],
    
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
            {
                test: /\.ejs$/,
                loader: "ejs-loader"
            },
        ],
    },

    resolve: {
        modulesDirectories: ['node_modules', 'media/js'],
        extensions: ['', '.js']
    },
}
