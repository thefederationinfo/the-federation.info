var express = require('express'),
    https = require('https'),
    util = require('util'),
    expressValidator = require('express-validator'),
    scheduler = require('node-schedule'),
    db = require('./database');
var app = express();

app.engine('jade', require('jade').renderFile);
app.set('title', 'Diaspora* Hub');
app.use(expressValidator([]));
app.use(express.static(__dirname + '/static'));

app.get('/', function(req, res) {
    var data = db.Pod.allForList(function(pods) {
        res.render('index.jade', { data: pods });
    },
    function(err, data) {
    });
});

app.get('/stats/:item', function(req, res) {
    if (['total_users', 'active_users_halfyear', 'active_users_monthly', 'local_posts'].indexOf(req.params.item) > -1) {
        db.Pod.allPodStats(req.params.item, function(stats) {
            var json = [];
            var podids = {};
            for (var i=0; i<stats.length; i++) {
                if (stats[i].item) {
                    if (typeof podids[stats[i].pod_id] === 'undefined') {
                        json.push({
                            name: stats[i].name,
                            data: [ ],
                            // following tip from http://stackoverflow.com/a/1152508/1489738
                            color: '#'+(0x1000000+(Math.random())*0xffffff).toString(16).substr(1,6)
                        });
                        podids[stats[i].pod_id] = json.length-1;
                    }
                    json[podids[stats[i].pod_id]].data.push({ x: stats[i].timestamp, y: stats[i].item });
                }
            }
            res.json(json);
        }, function (err, result) {
            if (err) console.log(err);
        });
    } else {
        res.json('[]');
    }
});

function callPod(podhost) {
    var options = {
        host: podhost,
        port: 443,
        path: '/statistics.json',
        method: 'GET'
    };
    var request = https.request(options, function(res) {
        console.log('STATUS: ' + res.statusCode);
        console.log('HEADERS: ' + JSON.stringify(res.headers));
        res.setEncoding('utf8');
        res.on('data', function (data) {
            try {
                data = JSON.parse(data);
                if (typeof data.version !== 'undefined') {
                    db.Pod.exists({ host: podhost }, function (err, exists) {
                        if (! exists) {
                            // Insert
                            db.Pod.create({
                                name: data.name,
                                host: podhost,
                                version: data.version,
                                registrations_open: data.registrations_open,
                                failures: 0,
                            }, function (err, items) {
                                if (err)
                                    console.log("Database error when inserting pod: "+err);
                                else
                                    items.logStats(data);
                            });
                        } else {
                            // Check for changes
                            db.Pod.find({ host: podhost }, function(err, pods) {
                                pod = pods[0];
                                if (pod.failures > 0 || pod.needsUpdate(data.name, data.version, data.registrations_open)) {
                                    pod.name = data.name;
                                    pod.version = data.version;
                                    pod.registrations_open = data.registrations_open;
                                    pod.failures = 0;   // reset counter
                                    pod.save(function(err) {
                                        if (err) console.log(err);
                                    });
                                };
                                pod.logStats(data);
                            });
                        }
                    });
                } else {
                    throw err;
                }
            } catch (err) {
                console.log('not a valid statistics json');
                // if this pod is known, log a failure
                db.Pod.exists({ host: podhost }, function (err, exists) {
                    if (exists) {
                        db.Pod.find({ host: podhost }, function(err, pods) {
                            pods[0].logFailure();
                        });
                    }
                });
            }
        });
    });
    request.end();
    request.on('error', function(e) {
        console.error(e);
    });
}

app.get('/register/:podhost', function(req, res) {
    console.log(req.ip);
    
    req.assert('podhost', 'Invalid pod url').isUrl().len(1, 100);
    var errors = req.validationErrors();
    if (errors) {
        res.send('There have been validation errors: ' + util.inspect(errors), 400);
        return;
    }

    callPod(req.params.podhost);
    
    res.type('text/plain');
    res.send('register received');
});

// Scheduling
var updater = scheduler.scheduleJob('7 0 * * *', function() {
    console.log('Calling pods for an update..');
    
    db.Pod.find({}, function(err, pods) {
        for (var i=0; i<pods.length; i++) {
            callPod(pods[i].host);
        }
    });
});

app.listen(process.env.PORT || 4730);
