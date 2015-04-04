/*jslint todo: true, node: true, stupid: true, plusplus: true, continue: true */
"use strict";
var mailer = {},
    transport = null,
    nodemailer = require('nodemailer'),
    smtpTransport = require("nodemailer-smtp-transport"),
    config = require('./config');

mailer.get_transport = function() {
    if (! transport) {
        transport = nodemailer.createTransport(
            smtpTransport({
                host: config.email.host,
                port: config.email.port,
                auth: {
                    user: config.email.username,
                    pass: config.email.password
                }
            })
        );
    }
    return transport;
};

mailer.send_mail = function(mail) {
    var transporter = mailer.get_transport();
    transporter.sendMail(mail);
};

module.exports = mailer;
