var routes = {};

routes.root = function(req, res, db) {
    var data = db.Pod.allForList(function(pods) {
        res.render('index.jade', { data: pods });
    },
    function(err, data) {
    });
}

routes.pods = function(req, res, db) {
    var data = db.Pod.allForList(
        function(pods) {
            res.json(pods);
        },
        function(err, result) {
            if (err) console.log(err);
        }
    );
}

routes.item = function(req, res, db) {
    if (['total_users', 'active_users_halfyear', 'active_users_monthly', 'local_posts'].indexOf(req.params.item) > -1) {
        db.Pod.allPodStats(req.params.item, function(stats) {
            var json = [];
            var podids = {};
            for (var i=0; i<stats.length; i++) {
                if (stats[i].item) {
                    if (typeof podids[stats[i].pod_id] === 'undefined') {
                        json.push({
                            name: (stats[i].name.toLowerCase() == 'diaspora*') ? stats[i].host : stats[i].name,
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
    } else if (req.params.item == 'global_users') {
        db.GlobalStat.getStats(function (stats) {
            var json = [ 
                { 
                    name: "Total users",
                    data: [],
                    color: '#'+(0x1000000+(Math.random())*0xffffff).toString(16).substr(1,6),
                    renderer: 'line'
                }
            ];
            for (var i=0; i<stats.length; i++) {
                json[0].data.push({ x: stats[i].timestamp, y: (stats[i].total_users) ? stats[i].total_users : 0 });
            }
            res.json(json);
        });
    } else if (req.params.item == 'global_posts') {
        db.GlobalStat.getStats(function (stats) {
            var json = [ 
                { 
                    name: "Total posts",
                    data: [],
                    color: '#'+(0x1000000+(Math.random())*0xffffff).toString(16).substr(1,6),
                    renderer: 'line'
                }
            ];
            for (var i=0; i<stats.length; i++) {
                json[0].data.push({ x: stats[i].timestamp, y: (stats[i].local_posts) ? stats[i].local_posts : 0 });
            }
            res.json(json);
        });
    } else if (req.params.item == 'global_active_month') {
        db.GlobalStat.getStats(function (stats) {
            var json = [ 
                { 
                    name: "Active users 1 month",
                    data: [],
                    color: '#'+(0x1000000+(Math.random())*0xffffff).toString(16).substr(1,6),
                    renderer: 'line'
                }
            ];
            for (var i=0; i<stats.length; i++) {
                json[0].data.push({ x: stats[i].timestamp, y: (stats[i].active_users_monthly) ? stats[i].active_users_monthly : 0 });
            }
            res.json(json);
        });
    } else if (req.params.item == 'global_active_halfyear') {
        db.GlobalStat.getStats(function (stats) {
            var json = [ 
                { 
                    name: "Active users 6 months",
                    data: [],
                    color: '#'+(0x1000000+(Math.random())*0xffffff).toString(16).substr(1,6),
                    renderer: 'line'
                }
            ];
            for (var i=0; i<stats.length; i++) {
                json[0].data.push({ x: stats[i].timestamp, y: (stats[i].active_users_halfyear) ? stats[i].active_users_halfyear : 0 });
            }
            res.json(json);
        });
    } else {
        res.json('[]');
    }
}

routes.register = function(req, res, db) {
    req.assert('podhost', 'Invalid pod url').isUrl().len(1, 100);
    var errors = req.validationErrors();
    if (errors) {
        res.send('There have been validation errors: ' + util.inspect(errors), 400);
        return false;
    }
    res.type('text/plain');
    res.send('register received, if this is a valid pod with suitable code, it will be visible at http://pods.jasonrobinson.me in a few seconds..');
    return req.params.podhost;
}

module.exports = routes;