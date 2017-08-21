/* jslint todo: true, node: true, stupid: true, plusplus: true, continue: true */
"use strict";
var orm = require("orm"),
    util = require("util"),
    config = require("./config"),
    fs = require("fs"),
    events = require("events"),
    mysql = require("mysql"),
    geoip = require("geoip-lite"),
    spawn = require("child_process").spawn,
    models = {},
    eventEmitter = new events.EventEmitter(),
    utils = require("./utils");

function setUpModels(db) {
    function execQueryWithCallback(query, params, callback) {
        db.driver.execQuery(query, params,
            function (err, data) {
                if (err) {
                    console.log(err);
                }
                callback(data);
            });
    }

    function chartQuery(complete) {
        return "SELECT timestamp, nodes, users, active_users_halfyear, active_users_monthly, local_posts, local_comments,\
          users / NULLIF(nodes, 0) AS users_per_node,\
          active_users_monthly / NULLIF(users, 0) AS active_users_ratio,\
          local_posts / NULLIF(users, 0) AS posts_per_user,\
          local_comments / NULLIF(users, 0) AS comments_per_user \
          FROM (SELECT UNIX_TIMESTAMP(date) AS timestamp,\
           COUNT(pod_id) AS nodes,\
           SUM(total_users) AS users,\
           SUM(active_users_halfyear) AS active_users_halfyear,\
           SUM(active_users_monthly) AS active_users_monthly,\
           SUM(local_posts) AS local_posts,\
           SUM(local_comments) AS local_comments \
           FROM stats s" + complete + " GROUP BY date) temp";
    }

    // set up models
    models.Pod = db.define("pods", {
        name: { type: "text", size: 300 },
        // due to this bug (https://github.com/dresende/node-orm2/issues/326) host not set unique yet..
        host: { type: "text", size: 100 },
        version: { type: "text", size: 30 },
        registrations_open: { type: "boolean" },
        failures: { type: "number" },
        ip4: { type: "text", size: 15 },
        country: { type: "text", size: 10 },
        network: { type: "text", size: 80 },
        service_facebook: { type: "number" },
        service_twitter: { type: "number" },
        service_tumblr: { type: "number" },
        service_wordpress: { type: "number" }
    }, {
        methods: {
            needsUpdate: function (data) {
                var checkKeys = [
                        "name", "version", "registrations_open", "ip4", "network", "service_facebook", "service_twitter",
                        "service_wordpress", "service_tumblr"
                    ], that = this;
                try {
                    checkKeys.forEach(function (key) {
                        if (data.network === undefined) {
                            data.network = "unknown";
                        }
                        utils.logger("db", "Pod.needsUpdate", "DEBUG", that.host + ": comparing " + key + " (old <-> new): " + that[key] + " <-> " + data[key]);
                        if (that[key] !== data[key]) {
                            throw "Update needed";
                        }
                    });
                } catch (updateNeeded) {
                    return true;
                }
                return false;
            },
            logStats: function (data) {
                var podId = this.id,
                    today = new Date();
                models.Stat.find({ pod_id: this.id, date: new Date(today.getFullYear(), today.getMonth(), today.getDate()) }, function (err, stats) {
                    if (err) {
                        console.log("Database error when finding stat: " + err);
                    }
                    if (!stats.length) {
                        if (!isNaN(data.total_users) || !isNaN(data.active_users_halfyear) || !isNaN(data.active_users_monthly) || isNaN(data.local_posts) || isNaN(data.local_comments)) {
                            models.Stat.create({
                                date: new Date(),
                                total_users: (isNaN(data.total_users)) ? 0 : data.total_users,
                                active_users_halfyear: (isNaN(data.active_users_halfyear)) ? 0 : data.active_users_halfyear,
                                active_users_monthly: (isNaN(data.active_users_monthly)) ? 0 : data.active_users_monthly,
                                local_posts: (isNaN(data.local_posts)) ? 0 : data.local_posts,
                                local_comments: (isNaN(data.local_comments)) ? 0 : data.local_comments,
                                pod_id: podId
                            }, function (err) {
                                if (err) {
                                    console.log("Database error when inserting stat: " + err);
                                }
                            });
                        }
                    }
                });
            },
            logFailure: function () {
                this.failures += 1;
                this.save(function (err) {
                    if (err) {
                        console.log(err);
                    }
                });
                if (this.failures < 3) {
                    // copy last stats too, if none exist yet
                    var today = new Date();
                    var podId = this.id;
                    var filter = {
                        pod_id: podId, date: new Date(today.getFullYear(), today.getMonth(), today.getDate()),
                    };
                    models.Stat.find(filter, function (err, stats) {
                        if (err) {
                            console.log("Database error when finding stat: " + err);
                        }
                        if (!stats.length) {
                            // no stats for today, get previous day and insert
                            var d = new Date();
                            d.setDate(d.getDate() - 1);
                            filter = { pod_id: podId, date: new Date(d.getFullYear(), d.getMonth(), d.getDate()) };
                            models.Stat.find(filter, function (err, stats) {
                                if (err) {
                                    console.log(err);
                                }
                                if (stats.length) {
                                    models.Stat.create({
                                        date: new Date(),
                                        total_users: stats[0].total_users,
                                        active_users_halfyear: stats[0].active_users_halfyear,
                                        active_users_monthly: stats[0].active_users_monthly,
                                        local_posts: stats[0].local_posts,
                                        local_comments: stats[0].local_comments,
                                        pod_id: stats[0].pod_id,
                                    }, function (err) {
                                        if (err) {
                                            console.log("Database error when copying previous stat: " + err);
                                        }
                                    });
                                }
                            });
                        }
                    });
                }
            },
            getCountry: function () {
                if (this.ip4) {
                    var geo = geoip.lookup(this.ip4);
                    if (geo && geo.country !== undefined && geo.country) {
                        this.country = geo.country;
                        utils.logger("db", "Pod.getCountry", "INFO", this.host + ": Country: " + geo.country);
                        this.save(function (err) {
                            if (err) {
                                utils.logger("db", "Pod.getCountry", "ERROR", this.host + ": Trying to save pod country: " + err);
                            }
                        });
                    } else {
                        utils.logger("db", "Pod.getCountry", "DEBUG", this.host + ": Nothing found? " + geo);
                    }
                }
            }
        }
    });
    models.Pod.projectStats = function (projectName, callback) {
        execQueryWithCallback("SELECT COUNT(p.id) AS nodes, SUM(total_users) AS users FROM stats s, pods p WHERE s.pod_id = p.id AND p.network = ? GROUP BY date ORDER BY date DESC LIMIT 1",
            [projectName], callback);
    };
    models.Pod.globalCharts = function (callback) {
        var query = chartQuery("");
        execQueryWithCallback(chartQuery(), [], callback);
    };
    models.Pod.projectCharts = function (projectName, callback) {
        var query = chartQuery(", pods p WHERE s.pod_id = p.id AND p.network = ?");
        execQueryWithCallback(query, [projectName], callback);
    };
    models.Pod.nodeCharts = function (nodeHost, callback) {
        var query = chartQuery(", pods p WHERE s.pod_id = p.id AND p.host = ?");
        execQueryWithCallback(query, [nodeHost], callback);
    };
    models.Pod.nodeInfo = function (nodeHost, callback) {
        execQueryWithCallback("SELECT * FROM pods WHERE host = ?", [nodeHost], callback);
    };
    models.Pod.allForList = function (projectName, callback) {
        var query =
          "SELECT p.id, p.name, p.host, p.version, p.registrations_open, p.country, p.network,\
              p.service_facebook, p.service_twitter, p.service_tumblr, p.service_wordpress,\
              (select total_users from stats where pod_id = p.id order by id desc limit 1) as total_users,\
              (select active_users_halfyear from stats where pod_id = p.id order by id desc limit 1) as active_users_halfyear,\
              (select active_users_monthly from stats where pod_id = p.id order by id desc limit 1) as active_users_monthly,\
              (select local_posts from stats where pod_id = p.id order by id desc limit 1) as local_posts,\
              (select local_comments from stats where pod_id = p.id order by id desc limit 1) as local_comments FROM pods p \
                  where failures < 3";
        if (projectName != undefined && projectName != "") {
            query += " AND p.network = '" + projectName + "'";
        }
        query += " ORDER BY active_users_monthly DESC";
        execQueryWithCallback(query, [], callback);
    };
    models.Pod.allPodStats = function (item, callback) {
        execQueryWithCallback(
            "SELECT p.name, p.host, s.pod_id, unix_timestamp(s.date) as timestamp, s." + item + " as item FROM pods p, stats s where p.failures < 3 and p.id = s.pod_id order by s.date",
            [], callback);
    };
    models.Stat = db.define("stats", {
        date: { type: "date", time: false },
        total_users: { type: "number" },
        active_users_halfyear: { type: "number" },
        active_users_monthly: { type: "number" },
        local_posts: { type: "number" },
        local_comments: { type: "number" }
    });
    models.Stat.hasOne("pod", models.Pod, { reverse: "stats" });
    models.GlobalStat = db.define("global_stats", {
        date: { type: "date", time: false },
        total_users: { type: "number" },
        active_users_halfyear: { type: "number" },
        active_users_monthly: { type: "number" },
        local_posts: { type: "number" },
        local_comments: { type: "number" },
        new_users: { type: "number" },
        new_posts: { type: "number" },
        new_comments: { type: "number" },
        pod_count: { type: "number" }
    });
    models.GlobalStat.logStats = function () {
        var d = new Date(),
            curDate = d.getFullYear() + "-" + (d.getMonth() + 1) + "-" + d.getDate();
        models.GlobalStat.exists({ date: curDate }, function (err, exists) {
            if (err) {
                console.log(err);
            } else if (!exists) {
                models.Stat.aggregate({ date: curDate }).sum("total_users").sum("active_users_halfyear").sum("active_users_monthly").sum("local_posts").sum("local_comments").count().get(function (err, total_users, active_users_halfyear, active_users_monthly, local_posts, local_comments, count) {
                    if (err) {
                        console.log(err);
                    }
                    d = new Date();
                    d.setDate(d.getDate() - 1);
                    var data = {
                            date: new Date(),
                            total_users: total_users,
                            active_users_monthly: active_users_monthly,
                            active_users_halfyear: active_users_halfyear,
                            local_posts: local_posts,
                            local_comments: local_comments,
                            pod_count: count
                        }, prevDate = d.getFullYear() + "-" + (d.getMonth() + 1) + "-" + d.getDate();
                    models.Stat.exists({ date: prevDate }, function (err, exists) {
                        if (err) {
                            console.log(err);
                        }
                        if (exists) {
                            models.Stat.aggregate({ date: prevDate }).sum("total_users").sum("local_posts").sum("local_comments").get(function (err, total_users, local_posts, local_comments) {
                                if (err) {
                                    console.log(err);
                                }
                                data.new_users = data.total_users - total_users;
                                data.new_posts = data.local_posts - local_posts;
                                data.new_comments = data.local_comments - local_comments;
                                models.GlobalStat.create(data, function (err) {
                                    if (err) {
                                        console.log("Database error when global stat: " + err);
                                    }
                                });
                            });
                        } else {
                            data.new_users = 0;
                            data.new_posts = 0;
                            data.new_comments = 0;
                            models.GlobalStat.create(data, function (err) {
                                if (err) {
                                    console.log("Database error when global stat: " + err);
                                }
                            });
                        }
                    });
                });
            }
        });
    };
    models.GlobalStat.getStats = function (callback) {
        execQueryWithCallback(
            "SELECT unix_timestamp(date) as timestamp, total_users, local_posts, local_comments, active_users_halfyear, active_users_monthly, pod_count FROM global_stats where date >= '2014-01-23' order by date",
            [], callback);
    };
    models.Pod.sync(function (err) {
        if (err) {
            console.log(err);
        }
    });
    models.Stat.sync(function (err) {
        if (err) {
            console.log(err);
        }
    });
    models.GlobalStat.sync(function (err) {
        if (err) {
            console.log(err);
        }
    });
}

function doMigration(migrations, migrdb, db) {
    var migration = migrations.shift(),
        python = null;
    console.log("processing: " + migration.name);
    if (migration.fakemigrations) {
        console.log("faked migration!");
        models.Migration.create({
            number: migration.number,
            name: migration.name,
            timestamp: new Date()
        }, function (err) {
            if (err) {
                console.log("Database error when inserting migration: " + err);
            }
        });
        if (migrations.length) {
            // do next
            doMigration(migrations, migrdb, db);
        } else {
            // no more, set up models
            console.log("** Migrations done, launching app.. **");
            eventEmitter.emit("migrations-done", db);
            migrdb.end();
        }
    } else if (migration.type === "sql") {
        migrdb.query(migration.sql, function (err) {
            if (err) {
                // migration failed
                console.log("Error: " + err.message);
                migrdb.rollback(function () {
                    throw err;
                });
            } else {
                migrdb.commit(function (err) {
                    if (err) {
                        migrdb.rollback(function () {
                            throw err;
                        });
                    }
                    console.log("success!");
                    models.Migration.create({
                        number: migration.number,
                        name: migration.name,
                        timestamp: new Date()
                    }, function (err) {
                        if (err) {
                            console.log("Database error when inserting migration: " + err);
                        }
                    });
                    if (migrations.length) {
                        // do next
                        doMigration(migrations, migrdb, db);
                    } else {
                        // no more, set up models
                        console.log("** Migrations done, launching app.. **");
                        eventEmitter.emit("migrations-done", db);
                        migrdb.end();
                    }
                });
            }
        });
    } else if (migration.type === "py") {
        python  = spawn("python", [ migration.filename ]);
        python.stdout.on("data", function (data) {
            console.log("stdout: " + data);
        });
        python.stderr.on("data", function (data) {
            console.log("stderr: " + data);
        });
        python.on("close", function (code) {
            console.log(code);
            if (code !== 0) {
                // migration failed
                console.log("Non-zero exit code from Python: " + code);
                throw "error";
            }
            console.log("success!");
            models.Migration.create({
                number: migration.number,
                name: migration.name,
                timestamp: new Date()
            }, function (err) {
                if (err) {
                    console.log("Database error when inserting migration: " + err);
                }
            });
            if (migrations.length) {
                // do next
                doMigration(migrations, migrdb, db);
            } else {
                // no more, set up models
                console.log("** Migrations done, launching app.. **");
                eventEmitter.emit("migrations-done", db);
                migrdb.end();
            }
        });
    }
}

function logGlobalStats() {
    /* Helper method to log global stats */
    utils.logger("database", "logGlobalStats", "INFO", "Updating global stats..");
    models.GlobalStat.logStats();
    utils.logger("database", "logGlobalStats", "INFO", "..done");
}

orm.connect("mysql://" + config.db.user + ":" + config.db.password + "@" + config.db.host + "/" + config.db.database + "?pool=true", function (err, db) {
    if (err) {
        console.log("Something is wrong with the db connection", err);
        return;
    }

    // check for migrations before setting up models
    models.Migration = db.define("migrations", {
        number: { type: "number" },
        name: { type: "text" },
        timestamp: { type: "date" }
    });
    models.Migration.sync(function (err) {
        if (err) {
            console.log(err);
            throw err;
        }
    });
    // listen to migrations done and launch models setup when we get that
    eventEmitter.on("migrations-done", setUpModels);
    // Trigger global stats update on migrations done
    eventEmitter.on("migrations-done", logGlobalStats);
    // get migrations
    models.Migration.find({}, function (error, result) {
        if (error) {
            console.log(error);
        }
        var migratefiles = fs.readdirSync("migrations/").sort(),
            fakemigrations = false,
            dbconfig = null,
            migrdb = null,
            migrations = [],
            i = 0,
            j = 0,
            done = false,
            migration = null,
            sql = null;
        if (!result.length) {
            // no migration history -- initial run, just fake all migrations
            fakemigrations = true;
        }
        if (migratefiles.length) {
            // separate non-orm mysql connection for flexibility
            dbconfig = config.db;
            dbconfig.multipleStatements = true;
            migrdb = mysql.createConnection(dbconfig);
            migrdb.connect(function (err) {
                if (err) {
                    console.log(err);
                    throw err;
                }
            });
            migrdb.beginTransaction(function (err) {
                if (err) {
                    console.log(err);
                    throw err;
                }
                // collect migrations
                for (i = 0; i < migratefiles.length; i++) {
                    if (migratefiles[i].indexOf(".sql") > -1) {
                        migration = {
                            number: parseInt(migratefiles[i].split("-")[0], 10),
                            name: migratefiles[i].split("-")[1],
                            filename: "migrations/" + migratefiles[i],
                            type: "sql",
                            fakemigrations: fakemigrations
                        };
                    } else if (migratefiles[i].indexOf(".py") > -1) {
                        migration = {
                            number: parseInt(migratefiles[i].split("-")[0], 10),
                            name: migratefiles[i].split("-")[1],
                            filename: "migrations/" + migratefiles[i],
                            type: "py",
                            fakemigrations: fakemigrations
                        };
                    } else {
                        continue;
                    }
                    if (isNaN(migration.number)) {
                        continue;
                    }
                    if (result) {
                        done = false;
                        for (j = 0; j < result.length; j++) {
                            if (result[j].number === migration.number) {
                                // done already
                                done = true;
                                break;
                            }
                        }
                        if (done) {
                            continue;
                        }
                    }
                    if (migration.type === "sql") {
                        sql = fs.readFileSync(migration.filename, { encoding: "utf8" });
                        // Ensure migration runs in correct database
                        migration.sql = "USE " + config.db.database + "; " + sql;
                    }
                    migrations.push(migration);
                }
                // launch migrations if found
                if (migrations.length) {
                    doMigration(migrations, migrdb, db);
                } else {
                    eventEmitter.emit("migrations-done", db);
                    migrdb.end();
                }
            });
        } else {
            eventEmitter.emit("migrations-done", db);
        }
    });
});

module.exports = models;
