/*jslint todo: true, node: true, stupid: true, plusplus: true, continue: true, nomen: true */
"use strict";

var express = require('express'),
    expressValidator = require('express-validator'),
    scheduler = require('node-schedule'),
    db = require('./database'),
    config = require('./config'),
    routes = require('./routes'),
    utils = require('./utils'),
    network = require('./network'),
    nunjucks = require('nunjucks'),
    app = express();

var nunjucks_env = nunjucks.configure('src/views', {
    autoescape: true,
    express: app
});
nunjucks_env.addGlobal("utils", utils);

app.set("env", "production");
app.set("json spaces", 0);
app.use(expressValidator([]));
app.use(express.compress());
app.use(express.static(__dirname + '/../static'));

app.get('/', function (req, res) {
    routes.root(req, res, db);
});

app.get('/nodes', function (req, res) {
    routes.nodesList(req, res, db);
});

app.get('/info', function (req, res) {
    routes.info(req, res, db);
});

app.get('/diaspora', function (req, res) {
    routes.renderNetwork('diaspora', res, db);
});

app.get('/friendica', function (req, res) {
    routes.renderNetwork('friendica', res, db);
});

app.get('/hubzilla', function (req, res) {
    routes.renderNetwork('hubzilla', res, db);
});

app.get('/ganggo', function (req, res) {
    routes.renderNetwork('ganggo', res, db);
});

app.get('/node/:host', function (req, res) {
    routes.renderNode(req, res, db);
});

/* API routes */
app.get('/pods.json', function (req, res) {
    routes.pods(req, res, db);
});

app.get('/stats/:item', function (req, res) {
    routes.item(req, res, db);
});

app.get('/register/:podhost', function (req, res) {
    var podhost = routes.register(req, res, db);
    if (podhost) {
        network.callPod(podhost);
    }
});

// Scheduling
scheduler.scheduleJob(config.scheduler, network.callAllPods);
if (config.doActivePodsSync) {
    scheduler.scheduleJob(config.schedulerActivePodsSync, utils.syncActivePods);
}

app.listen(config.app.port);
console.log('The-Federation.info listening on http://127.0.0.1:' + config.app.port);
