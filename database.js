var orm = require('orm'),
    util = require('util'),
    config = require('./config'),
    models = {};

orm.connect("mysql://"+config.db.user+":"+config.db.password+"@"+config.db.host+"/"+config.db.database, function (err, db) {
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
                return (this.name === name && this.version === version && this.registrations_open === registrations_open);
            },
            logStats: function (data) {
                var podId = this.id;
                var today = new Date();
                models.Stat.find({ pod_id: this.id, date: new Date(today.getFullYear(), today.getMonth(), today.getDate()) }, function(err, stats) {
                    if (! stats.length) {
                        models.Stat.create({
                            date: new Date(),
                            total_users: parseInt(data.total_users),
                            active_users: parseInt(data.active_six_month_users),
                            local_posts: parseInt(data.local_posts),
                            pod_id: podId,
                        }, function (err, items) {
                            if (err)
                                console.log("Database error when inserting stat: "+err);
                        });
                    }
                });
            },
        }
    });
    models.Stat = db.define('stats', {
        date: { type: "date", time: false },
        total_users: { type: "number" },
        active_users: { type: "number" },
        local_posts: { type: "number" },
    })
    models.Stat.hasOne('pod', models.Pod, { reverse: 'stats' });
    
    models.Pod.sync(function (err) {
        if (err) console.log(err);
    });
    models.Stat.sync(function (err) {
        if (err) console.log(err);
    });
});

module.exports = models;