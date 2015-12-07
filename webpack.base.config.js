var path = require("path")
var webpack = require('webpack')

module.exports = {
    context: __dirname,

    plugins: [
        new webpack.ProvidePlugin({
            _: "underscore"
        })
    ],
    
    entry: [
        "!style!css!less!bootstrap/less/bootstrap.less",
        "bootstrap-webpack!./bootstrap.config.js",
        './media/js/main',
    ],

    output: {
        path: path.resolve('./media/js/dist/'),
        sourceMapFilename: "[name].map",
        filename: "[name].js",
    },
    
    module: {
        loaders: [
            { test: /\.ejs$/, loader: "ejs-loader" },
            { test: /bootstrap\/js\//, loader: 'imports?jQuery=jquery' },
            { test: /\.css$/, loader: 'style-loader!css-loader' },
            { test: /\.less$/, loader: "style!css!less" },
            { test: /\.(woff|woff2)(\?v=\d+\.\d+\.\d+)?$/, loader: "url?limit=10000&mimetype=application/font-woff" },
            { test: /\.ttf(\?v=\d+\.\d+\.\d+)?$/, loader: "url?limit=10000&mimetype=application/octet-stream" },
            { test: /\.eot(\?v=\d+\.\d+\.\d+)?$/, loader: "file" },
            { test: /\.svg(\?v=\d+\.\d+\.\d+)?$/, loader: "url?limit=10000&mimetype=image/svg+xml" }
        ],
    },

    resolve: {
        modulesDirectories: ['node_modules', 'media/js'],
        extensions: ['', '.js']
    },
}
