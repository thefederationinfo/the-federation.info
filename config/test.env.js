'use strict'
const merge = require('webpack-merge')
const devEnv = require('./dev.env')

module.exports = merge(devEnv, {
    API_URI: '"http://127.0.0.1:8000/graphql"',
    NODE_ENV: '"testing"',
})
