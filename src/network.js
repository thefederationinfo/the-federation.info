/*jslint todo: true, node: true, stupid: true, plusplus: true, continue: true */
"use strict";

var network = {},
    https = require('https'),
    dns = require('dns'),
    url = require("url"),
    utils = require('./utils'),
    db = require('./database');


function getPodDataFromStatisticsJSON(host, data) {
    return {
        name: data.name,
        host: host,
        version: data.version,
        registrations_open: data.registrations_open,
        failures: 0,
        network: data.network || "unknown",
        service_facebook: (data.facebook) ? 1 : 0,
        service_twitter: (data.twitter) ? 1 : 0,
        service_tumblr: (data.tumblr) ? 1 : 0,
        service_wordpress: (data.wordpress) ? 1 : 0,
        ip4: data.ip4
    };
}

function getPodDataFromNodeInfo(host, data) {
    return {
        name: data.metadata.nodeName,
        host: host,
        version: data.software.version,
        registrations_open: data.openRegistrations,
        failures: 0,
        network: data.software.name,
        service_facebook: (data.services.outbound.indexOf("facebook") > -1)  ? 1 : 0,
        service_twitter: (data.services.outbound.indexOf("twitter") > -1) ? 1 : 0,
        service_tumblr: (data.services.outbound.indexOf("tumblr") > -1) ? 1 : 0,
        service_wordpress: (data.services.outbound.indexOf("wordpress") > -1) ? 1 : 0,
        ip4: data.ip4
    };
}

function getPodDataFromResponse(host, data, callType) {
    if (callType == "nodeinfo") {
        return getPodDataFromNodeInfo(host, data);
    } else {
        return getPodDataFromStatisticsJSON(host, data);
    }
}

function getPodStatsFromStatisticsJSON(data) {
    return {
        total_users: data.total_users,
        active_users_halfyear: data.active_users_halfyear,
        active_users_monthly: data.active_users_monthly,
        local_posts: data.local_posts
    }
}

function getPodStatsFromNodeInfo(data) {
    return {
        total_users: data.usage.users.total,
        active_users_halfyear: data.usage.users.activeHalfyear,
        active_users_monthly: data.usage.users.activeMonth,
        local_posts: data.usage.localPosts
    }
}

function getPodStatsFromResponse(data, callType) {
    if (callType == "nodeinfo") {
        return getPodStatsFromNodeInfo(data);
    } else {
        return getPodStatsFromStatisticsJSON(data);
    }
}

network.handleCallResponse = function(podhost, data, callType) {
    data = JSON.parse(data);
    console.log(data);
    if (data.version !== undefined) {
        db.Pod.exists({ host: podhost }, function (err, exists) {
            if (err) {
                console.log(err);
            }
            dns.resolve4(podhost, function (err, addresses) {
                if (err) {
                    utils.logger('app', 'handleCallResponse', 'ERROR', podhost + ': ' + err);
                    data.ip4 = null;
                } else {
                    data.ip4 = addresses[0];
                }
                var responseData = getPodDataFromResponse(podhost, data, callType);
                var podStats = getPodStatsFromResponse(data, callType);
                if (!exists) {
                    // Insert
                    db.Pod.create(responseData, function (err, items) {
                        if (err) {
                            utils.logger('app', 'handleCallResponse', 'ERROR',
                                podhost + ': Database error when inserting pod: ' + err);
                        } else {
                            items.getCountry();
                            items.logStats(podStats);
                        }
                    });
                } else {
                    // Check for changes
                    db.Pod.find({ host: podhost }, function (err, pods) {
                        if (err) {
                            console.log(err);
                        }
                        var pod = pods[0];
                        if (pod.failures > 0 || pod.needsUpdate(responseData)) {
                            utils.logger('app', 'handleCallResponse', 'INFO', podhost + ': UPDATING');
                            pod.save(responseData, function (err) {
                                if (err) {
                                    utils.logger('app', 'handleCallResponse', 'ERROR',
                                        podhost + ': Trying to save pod update: ' + err);
                                } else {
                                    pod.getCountry();
                                }
                            });
                        } else {
                            utils.logger('app', 'handleCallResponse', 'INFO', podhost + ': no updates');
                        }
                        pod.logStats(podStats);
                    });
                }
            });
        });
    } else {
        throw "error";
    }
};

network.callStatisticsJSON = function(podhost) {
    var options = {
        host: podhost,
        port: 443,
        path: '/statistics.json',
        method: 'GET',
        agent: false,
        rejectUnauthorized: false
    };
    utils.logger('app', 'callStatisticsJSON', 'INFO', podhost + ': Calling for statistics.json');
    var request = https.request(options, function (res) {
        utils.logger('app', 'callStatisticsJSON', 'DEBUG', podhost + ': STATUS: ' + res.statusCode);
        utils.logger('app', 'callStatisticsJSON', 'DEBUG', podhost + ': HEADERS: ' + JSON.stringify(res.headers));
        if (res.statusCode === 404) {
            utils.logger('app', 'callStatisticsJSON', 'ERROR', podhost + ': not statistics.json found');
            network.logKnownPodFailure(podhost);
        } else {
            res.setEncoding('utf8');
            res.on('data', function (data) {
                try {
                    network.handleCallResponse(podhost, data, "statistics.json");
                } catch (err) {
                    utils.logger('app', 'callStatisticsJSON', 'ERROR', podhost + ': not a valid statistics json');
                    network.logKnownPodFailure(podhost);
                }
            });
        }
    });
    request.end();
    request.on('error', function (e) {
        utils.logger('app', 'callStatisticsJSON', 'ERROR', podhost + ': ' + e);
        network.logKnownPodFailure(podhost);
    });
};

function getNodeInfoURL(response) {
    try {
        response = JSON.parse(response);
        // Yes, there is a better way, but for now just take the first
        return response.links[0].href;
    } catch (err) {
        return null;
    }
}

network.callNodeInfo = function(podhost) {
    var options = {
        host: podhost,
        port: 443,
        path: '/.well-known/nodeinfo',
        method: 'GET',
        agent: false,
        rejectUnauthorized: false
    };
    utils.logger('app', 'callNodeInfo', 'INFO', podhost + ': Calling for NodeInfo');
    var request = https.request(options, function (res) {
        utils.logger('app', 'callNodeInfo', 'DEBUG', podhost + ': STATUS: ' + res.statusCode);
        utils.logger('app', 'callNodeInfo', 'DEBUG', podhost + ': HEADERS: ' + JSON.stringify(res.headers));
        if (res.statusCode === 404) {
            // Fallback to statistics.json
            utils.logger('app', 'callNodeInfo', 'DEBUG', podhost + ': nodeinfo not supported');
            network.callStatisticsJSON(podhost);
        } else {
            res.setEncoding('utf8');
            res.on('data', function (data) {
                var nodeInfoUrl = getNodeInfoURL(data);
                if (nodeInfoUrl) {
                    var parsedUrl = url.parse(nodeInfoUrl);
                    options.host = parsedUrl.hostname;
                    options.path = parsedUrl.pathname;
                    utils.logger('app', 'callNodeInfo', 'INFO', podhost + ': NodeInfo URL: ' + nodeInfoUrl);
                    // request.end();
                    var nodeInfoRequest = https.request(options, function (res) {
                        utils.logger('app', 'callNodeInfo', 'DEBUG', podhost + ': STATUS: ' + res.statusCode);
                        utils.logger('app', 'callNodeInfo', 'DEBUG', podhost + ': HEADERS: ' + JSON.stringify(res.headers));
                        res.setEncoding('utf8');
                        res.on('data', function (data) {
                            try {
                                network.handleCallResponse(podhost, data, "nodeinfo");
                            } catch (err) {
                                utils.logger('app', 'callNodeInfo', 'ERROR', podhost + ': not a valid NodeInfo document');
                                // Fallback to statistics.json
                                network.callStatisticsJSON(podhost);
                            }
                        });
                    }).on('error', function (e) {
                        // Fallback to statistics.json
                        utils.logger('app', 'callNodeInfo', 'ERROR', podhost + ': ' + e);
                        network.callStatisticsJSON(podhost);
                    });
                    nodeInfoRequest.end();
                } else {
                    // Fallback to statistics.json
                    utils.logger('app', 'callNodeInfo', 'ERROR', podhost + ': no nodeinfo url found');
                    network.callStatisticsJSON(podhost);
                }
            });
        }
    });
    request.end();
    request.on('error', function (e) {
        // Fallback to statistics.json
        utils.logger('app', 'callNodeInfo', 'ERROR', podhost + ': ' + e);
        network.callStatisticsJSON(podhost);
    });
};

network.callPod = function(podhost) {
    utils.logger('app', 'callPod', 'INFO', podhost + ': Calling for update');
    network.callNodeInfo(podhost);
};

// Call all pods
network.callAllPods = function() {
    var i = 0,
        podhost = null;
    console.log('Calling pods for an update..');
    db.Pod.find({}, function (err, pods) {
        if (err) {
            console.log(err);
        }
        for (i = 0; i < pods.length; i++) {
            podhost = pods[i].host;
            setTimeout(network.callPod, Math.floor(Math.random() * 10000) + 1, podhost);
        }
        setTimeout(db.GlobalStat.logStats, 300000);
    });
};

network.logKnownPodFailure = function(podhost) {
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
};

module.exports = network;
