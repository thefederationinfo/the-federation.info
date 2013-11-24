var orm = require('orm'),
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
    });
    models.Pod.sync(function (err) {
        if (err) console.log(err);
    });
});

module.exports = models;