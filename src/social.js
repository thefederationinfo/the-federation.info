var _ = require("underscore");
var spawn = require("child_process").spawn;
var fs = require("fs");
var db = require("./database");
var config = require("./config");
var mailer = require("./mailer");

var social = {};

var templates = {
    "daily": _.template(
        "#### Daily statistics from The Federation\n" +
        "\n" +
        "* Nodes: <%= nodes %>\n" +
        "* Active users (6 months): <%= active_users_halfyear %>\n" +
        "* Active users (30 days): <%= active_users_monthly %>\n" +
        "* Total user accounts: <%= users %>\n" +
        "\n" +
        "For more detailed statistics visit [the-federation.info](https://the-federation.info).\n" +
        "\n" +
        "#thefederationstatsdaily"
    ),
};

social.post = function (message) {
    /* Post a message on Socialhome */
    var tempFile = "/tmp/thefederationshclipost.tmp";
    fs.writeFile(tempFile, message, function (err) {
        if (err) {
            return console.log("social.post: " + err);
        }

        var shcli = spawn("shcli", [
            "create", config.shcli.domain, config.shcli.token, "-f", tempFile, "-v", "public",
        ]);
        shcli.stdout.on("data", function (data) {
            console.log("shcli stdout: " + data);
        });
        shcli.stderr.on("data", function (data) {
            console.log("shcli stderr: " + data);
        });
        shcli.on("close", function (code) {
            console.log("shcli: Result is " + code);
            if (code !== 0) {
                // Error from shcli job, notify
                mailer.send_mail({
                    from: "do-not-reply@the-federation.info",
                    to: config.admin.email,
                    subject: "[warning] shcli command failed",
                    text: "shcli command failed with code: " + code,
                });
            }
            fs.unlinkSync(tempFile);
        });
        return true;
    });
};

social.dailyStatistics = function () {
    /* Collect daily statistics post */
    db.Pod.globalCharts(function (stats) {
        var message = templates.daily(stats[stats.length - 1]);
        social.post(message);
    });
};

module.exports = social;
