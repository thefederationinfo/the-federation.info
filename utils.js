var utils = {};

utils.get_pod_network_and_version = function(network, version) {
    /* Return an array that contains network and version
    by looking at network and version from pod data. These are
    not always filled properly. */
    if (typeof network === 'undefined')
        network = 'unknown';
    try {
        switch (network.toLowerCase()) {
            case "friendica":
                return ["friendica", version];
            case "redmatrix":
                return ["redmatrix", version];
            // pyaspora has no network id atm, fall to default
            case "pyaspora":
            // diaspora has no network id atm, fall to default
            case "diaspora":
            default:
                // diaspora, most likely
                if (version.indexOf('head') === 0)
                    // diaspora, development head
                    return ["diaspora", ".develop"];
                else if (version.indexOf('-') > -1)
                    // diaspora, maybe, normal, return version part only, no hash
                    return ["diaspora", version.split('-')[0]];
                else if (version.indexOf('x') > -1)
                    // pyaspora, maybe
                    return ["pyaspora", version];
                else {
                    // fallback, assume diaspora..
                    return ["diaspora", version];
                }
        }
    } catch (e) {
        utils.logger('utils', 'get_pod_network_and_version', 'ERROR', e);
        return ["unknown", version];
    }
}

utils.logger = function(module, object, level, msg) {
    /* Output to console some standard formatted logging */
    console.log(new Date() + ' - [' + level + '] ' + module + '.' + object + ' | ' + msg);
}

utils.services_string = function(pod) {
    /* Build a string for the Services column in the podlist */
    services = ["facebook", "twitter", "tumblr", "wordpress"];
    service_keys = ["fb", "tw", "tu", "wp"];
    enabled = [];
    for (var i=0; i<services.length; i++) {
        if (pod["service_"+services[i]] == 1)
            enabled.push(service_keys[i]);
    }
    return enabled.join(',');
}

module.exports = utils;
