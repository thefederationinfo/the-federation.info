var express = require('express'),
    https = require('https'),
    util = require('util'),
    expressValidator = require('express-validator'),
    scheduler = require('node-schedule'),
    db = require('./database'),
    dns = require('dns');
var app = express();

app.engine('jade', require('jade').renderFile);
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
    } else if (req.params.item == 'global') {
        db.GlobalStat.getStats(function (stats) {
            var json = [ 
                { 
                    name: "Active users 1 month",
                    data: [],
                    color: '#'+(0x1000000+(Math.random())*0xffffff).toString(16).substr(1,6),
                    renderer: 'stack'
                },
                { 
                    name: "Active users 6 months",
                    data: [],
                    color: '#'+(0x1000000+(Math.random())*0xffffff).toString(16).substr(1,6),
                    renderer: 'stack'
                },
                { 
                    name: "Total users",
                    data: [],
                    color: '#'+(0x1000000+(Math.random())*0xffffff).toString(16).substr(1,6),
                    renderer: 'stack'
                },
                { 
                    name: "Total posts",
                    data: [],
                    color: '#'+(0x1000000+(Math.random())*0xffffff).toString(16).substr(1,6),
                    renderer: 'line'
                }
            ];
            for (var i=0; i<stats.length; i++) {
                json[2].data.push({ x: stats[i].timestamp, y: (stats[i].total_users) ? stats[i].total_users : 0 });
                json[3].data.push({ x: stats[i].timestamp, y: (stats[i].local_posts) ? stats[i].local_posts : 0 });
                json[1].data.push({ x: stats[i].timestamp, y: (stats[i].active_users_halfyear) ? stats[i].active_users_halfyear : 0 });
                json[0].data.push({ x: stats[i].timestamp, y: (stats[i].active_users_monthly) ? stats[i].active_users_monthly : 0 });
            }
            res.json(json);
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
    res.send('register received, if this is a valid pod with suitable code, it will be visible at http://pods.jasonrobinson.me in a few seconds..');
});

// Scheduling
var updater = scheduler.scheduleJob('7 0 * * *', function() {
    console.log('Calling pods for an update..');
    
    db.Pod.find({}, function(err, pods) {
        for (var i=0; i<pods.length; i++) {
            var podhost = pods[i].host;
            setTimeout(callPod, Math.floor(Math.random() * 10000) +1, podhost);
        }
        setTimeout(db.GlobalStat.logStats, 45000);
    });
});

app.listen(process.env.PORT || 4730);
