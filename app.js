var express = require('express'),
    https = require('https'),
    util = require('util'),
    expressValidator = require('express-validator'),
    scheduler = require('node-schedule'),
    db = require('./database'),
    dns = require('dns'),
    config = require('./config'),
    routes = require('./routes');
var app = express();

app.engine('jade', require('jade').renderFile);
app.use(expressValidator([]));
app.use(express.static(__dirname + '/static'));

app.get('/', function(req, res) {
    routes.root(req, res, db);
});

app.get('/stats/:item', function(req, res) {
    routes.item(req, res, db);
});

app.get('/register/:podhost', function(req, res) {
    podhost = routes.register(req, res, db);
    if (podhost) {
        callPod(podhost);
    }
});

function logKnownPodFailure(podhost) {
    // if this pod is known, log a failure
    db.Pod.exists({ host: podhost }, function (err, exists) {
        if (exists) {
            db.Pod.find({ host: podhost }, function(err, pods) {
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
        rejectUnauthorized: false
    };
    console.log('');
    console.log('*** Calling for update: '+podhost)
    var request = https.request(options, function(res) {
        console.log('STATUS: ' + res.statusCode);
        console.log('HEADERS: ' + JSON.stringify(res.headers));
        res.setEncoding('utf8');
        res.on('data', function (data) {
            try {
                data = JSON.parse(data);
                if (typeof data.version !== 'undefined') {
                    db.Pod.exists({ host: podhost }, function (err, exists) {
                        dns.resolve4(podhost, function (err, addresses) {
                            if (err) {
                                console.log(err);
                                ip4 = null;
                            } else {
                                ip4 = addresses[0];
                            }
                            if (! exists) {
                                // Insert
                                db.Pod.create({
                                    name: data.name,
                                    host: podhost,
                                    version: data.version,
                                    registrations_open: data.registrations_open,
                                    failures: 0,
                                    ip4: ip4,
                                }, function (err, items) {
                                    if (err) {
                                        console.log("Database error when inserting pod: "+err);
                                    } else {
                                        items.getCountry();
                                        items.logStats(data);
                                    }
                                });
                            } else {
                                // Check for changes
                                db.Pod.find({ host: podhost }, function(err, pods) {
                                    console.log('-- New data:');
                                    console.log(data);
                                    console.log(ip4);
                                    pod = pods[0];
                                    console.log('-- Old data:')
                                    console.log(pod.failures);
                                    console.log(pod.name);
                                    console.log(pod.version);
                                    console.log(pod.registrations_open);
                                    console.log(pod.ip4);
                                    if (pod.failures > 0 || pod.needsUpdate(data.name, data.version, data.registrations_open, ip4)) {
                                        console.log('pod '+podhost+' update');
                                        pod.name = data.name;
                                        pod.version = data.version;
                                        pod.registrations_open = data.registrations_open;
                                        pod.failures = 0;   // reset counter
                                        pod.ip4 = ip4;
                                        pod.save(function(err) {
                                            if (err) {
                                                console.log(err);
                                            } else {
                                                pod.getCountry();
                                            }
                                        });
                                    } else {
                                        console.log('pod '+podhost+' no update');
                                    }
                                    pod.logStats(data);
                                });
                            }
                        });
                    });
                } else {
                    throw err;
                }
            } catch (err) {
                console.log('host '+podhost+' not a valid statistics json');
                logKnownPodFailure(podhost);
            }
        });
    });
    request.end();
    request.on('error', function(e) {
        console.error(e);
        logKnownPodFailure(podhost);
    });
}

// Scheduling
var updater = scheduler.scheduleJob(config.scheduler, function() {
    console.log('Calling pods for an update..');
    
    db.Pod.find({}, function(err, pods) {
        for (var i=0; i<pods.length; i++) {
            var podhost = pods[i].host;
            setTimeout(callPod, Math.floor(Math.random() * 10000) +1, podhost);
        }
        setTimeout(db.GlobalStat.logStats, 45000);
    });
});

app.listen(4730);
console.log('Diaspora-Hub listening on http://127.0.0.1:4730...');
