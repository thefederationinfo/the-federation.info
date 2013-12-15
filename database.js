var orm = require('orm'),
    util = require('util'),
    config = require('./config'),
    models = {};

orm.connect("mysql://"+config.db.user+":"+config.db.password+"@"+config.db.host+"/"+config.db.database+'?pool=true', function (err, db) {
    if (err) {
        console.log("Something is wrong with the db connection", err);
        return;
    }

    models.Pod = db.define('pods', {
        name: { type: "text", size: 300 },
        // due to this bug (https://github.com/dresende/node-orm2/issues/326) host not set unique yet..
        host: { type: "text", size: 100 },
        version: { type: "text", size: 30 },
        registrations_open: { type: "boolean" },
    }, {
        methods: {
            needsUpdate: function (name, version, registrations_open) {
                return (this.name !== name || this.version !== version || this.registrations_open !== registrations_open);
            },
            logStats: function (data) {
                var podId = this.id;
                var today = new Date();
                models.Stat.find({ pod_id: this.id, date: new Date(today.getFullYear(), today.getMonth(), today.getDate()) }, function(err, stats) {
                    if (! stats.length) {
                        if (! isNaN(data.total_users) || ! isNaN(data.active_users_halfyear) || ! isNaN(data.active_users_monthly) || isNaN(data.local_posts)) {
                            models.Stat.create({
                                date: new Date(),
                                total_users: (isNaN(data.total_users)) ? 0 : data.total_users,
                                active_users_halfyear: (isNaN(data.active_users_halfyear)) ? 0 : data.active_users_halfyear,
                                active_users_monthly: (isNaN(data.active_users_monthly)) ? 0 : data.active_users_monthly,
                                local_posts: (isNaN(data.local_posts)) ? 0 : data.local_posts,
                                pod_id: podId,
                            }, function (err, items) {
                                if (err)
                                    console.log("Database error when inserting stat: "+err);
                            });
                        }
                    }
                });
            },
        }
    });
    models.Pod.allForList = function (callback) {
        db.driver.execQuery(
            "SELECT p.name, p.host, p.version, p.registrations_open,\
                (select total_users from stats where pod_id = p.id order by id desc limit 1) as total_users,\
                (select active_users_halfyear from stats where pod_id = p.id order by id desc limit 1) as active_users_halfyear,\
                (select active_users_monthly from stats where pod_id = p.id order by id desc limit 1) as active_users_monthly,\
                (select local_posts from stats where pod_id = p.id order by id desc limit 1) as local_posts FROM pods p",
            [],
            function (err, data) {
                if (err) console.log(err);
                callback(data);
            }
        );
    };
    models.Pod.allPodStats = function (item, callback) {
        db.driver.execQuery(
            "SELECT p.name, s.pod_id, unix_timestamp(s.date) as timestamp, s."+item+" as item FROM pods p, stats s where p.id = s.pod_id order by s.date",
            [],
            function (err, data) {
                if (err) console.log(err);
                callback(data);
            }
        );
    };
    models.Stat = db.define('stats', {
        date: { type: "date", time: false },
        total_users: { type: "number" },
        active_users_halfyear: { type: "number" },
        active_users_monthly: { type: "number" },
        local_posts: { type: "number" },
    });
    models.Stat.hasOne('pod', models.Pod, { reverse: 'stats' });
    
    models.Pod.sync(function (err) {
        if (err) console.log(err);
    });
    models.Stat.sync(function (err) {
        if (err) console.log(err);
    });
});

module.exports = models;