/*jslint todo: true, node: true, stupid: true, plusplus: true, continue: true, nomen: true */
"use strict";
var express = require('express'),
    https = require('https'),
    expressValidator = require('express-validator'),
    scheduler = require('node-schedule'),
    db = require('./database'),
    dns = require('dns'),
    config = require('./config'),
    routes = require('./routes'),
    utils = require('./utils');
var app = express();

app.engine('jade', require('jade').renderFile);
app.locals.utils = utils;  // expose utils to jade
app.use(expressValidator([]));
app.use(express.static(__dirname + '/static'));

function logKnownPodFailure(podhost) {
    // if this pod is known, log a failure
    db.Pod.exists({ host: podhost }, function (err, exists) {
        if (err) {
            console.log(err);
        }
        if (exists) {
            db.Pod.find({ host: podhost }, function (err, pods) {
                if (err) {
                    console.log(err);
                }
                pods[0].logFailure();
            });
        }
    });
}

function callPod(podhost) {
    var options = {
        host: podhost,
        port: 443,
        path: '/statistics.json',
        method: 'GET',
        agent: false,
        rejectUnauthorized: false,
    }, request = null;
    utils.logger('app', 'callPod', 'INFO', podhost + ': Calling for update');
    request = https.request(options, function (res) {
        utils.logger('app', 'callPod', 'DEBUG', podhost + ': STATUS: ' + res.statusCode);
        utils.logger('app', 'callPod', 'DEBUG', podhost + ': HEADERS: ' + JSON.stringify(res.headers));
        res.setEncoding('utf8');
        res.on('data', function (data) {
            try {
                data = JSON.parse(data);
                if (data.version !== undefined) {
                    db.Pod.exists({ host: podhost }, function (err, exists) {
                        if (err) {
                            console.log(err);
                        }
                        dns.resolve4(podhost, function (err, addresses) {
                            if (err) {
                                utils.logger('app', 'callPod', 'ERROR', podhost + ': ' + err);
                                data.ip4 = null;
                            } else {
                                data.ip4 = addresses[0];
                            }
                            if (!exists) {
                                // Insert
                                db.Pod.create({
                                    name: data.name,
                                    host: podhost,
                                    version: data.version,
                                    registrations_open: data.registrations_open,
                                    failures: 0,
                                    ip4: data.ip4,
                                    network: data.network || 'unknown',
                                    service_facebook: (data.facebook) ? 1 : 0,
                                    service_twitter: (data.twitter) ? 1 : 0,
                                    service_tumblr: (data.tumblr) ? 1 : 0,
                                    service_wordpress: (data.wordpress) ? 1 : 0
                                }, function (err, items) {
                                    if (err) {
                                        utils.logger('app', 'callPod', 'ERROR', podhost + ': Database error when inserting pod: ' + err);
                                    } else {
                                        items.getCountry();
                                        items.logStats(data);
                                    }
                                });
                            } else {
                                // Check for changes
                                db.Pod.find({ host: podhost }, function (err, pods) {
                                    if (err) {
                                        console.log(err);
                                    }
                                    var pod = pods[0];
                                    if (pod.failures > 0 || pod.needsUpdate(data)) {
                                        utils.logger('app', 'callPod', 'INFO', podhost + ': UPDATING');
                                        pod.name = data.name;
                                        pod.version = data.version;
                                        pod.registrations_open = data.registrations_open;
                                        pod.failures = 0;   // reset counter
                                        pod.ip4 = data.ip4;
                                        pod.network = data.network || 'unknown';
                                        pod.service_facebook = (data.facebook) ? 1 : 0;
                                        pod.service_twitter = (data.twitter) ? 1 : 0;
                                        pod.service_tumblr = (data.tumblr) ? 1 : 0;
                                        pod.service_wordpress = (data.wordpress) ? 1 : 0;
                                        pod.save(function (err) {
                                            if (err) {
                                                utils.logger('app', 'callPod', 'ERROR', podhost + ': Trying to save pod update: ' + err);
                                            } else {
                                                pod.getCountry();
                                            }
                                        });
                                    } else {
                                        utils.logger('app', 'callPod', 'INFO', podhost + ': no updates');
                                    }
                                    pod.logStats(data);
                                });
                            }
                        });
                    });
                } else {
                    throw "error";
                }
            } catch (err) {
                utils.logger('app', 'callPod', 'ERROR', podhost + ': not a valid statistics json');
                console.log('host ' + podhost + ' not a valid statistics json');
                logKnownPodFailure(podhost);
            }
        });
    });
    request.end();
    request.on('error', function (e) {
        utils.logger('app', 'callPod', 'ERROR', podhost + ': ' + e);
        logKnownPodFailure(podhost);
    });
}


app.get('/', function (req, res) {
    routes.root(req, res, db);
});

app.get('/pods.json', function (req, res) {
    routes.pods(req, res, db);
});

app.get('/stats/:item', function (req, res) {
    routes.item(req, res, db);
});

app.get('/register/:podhost', function (req, res) {
    var podhost = routes.register(req, res, db);
    if (podhost) {
        callPod(podhost);
    }
});

// Call all pods
var callAllPods = function () {
    var i = 0,
        podhost = null;
    console.log('Calling pods for an update..');
    db.Pod.find({}, function (err, pods) {
        if (err) {
            console.log(err);
        }
        for (i = 0; i < pods.length; i++) {
            podhost = pods[i].host;
            setTimeout(callPod, Math.floor(Math.random() * 10000) + 1, podhost);
        }
        setTimeout(db.GlobalStat.logStats, 300000);
    });
};

// Scheduling
scheduler.scheduleJob(config.scheduler, callAllPods);

app.listen(4730);
console.log('Diaspora-Hub listening on http://127.0.0.1:4730...\nCalling all pods in 20s...');

// always do a full call to all pods on app init
setTimeout(callAllPods, 20000);
