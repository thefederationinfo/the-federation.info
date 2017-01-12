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

app.get('/global-stats.html', function (req, res) {
    routes.globalStatsPage(req, res, db);
});

app.get('/info.html', function (req, res) {
    routes.info(req, res, db);
});

app.get('/diaspora.html', function (req, res) {
    routes.diaspora(req, res, db);
});

app.get('/friendica.html', function (req, res) {
    routes.friendica(req, res, db);
});

app.get('/redmatrix.html', function (req, res) {
    routes.redmatrix(req, res, db);
});

app.get('/hubzilla.html', function (req, res) {
    routes.hubzilla(req, res, db);
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
scheduler.scheduleJob(config.schedulerActivePodsSync, utils.syncActivePods);

app.listen(4730);
console.log('The-Federation.info listening on http://127.0.0.1:4730...');
