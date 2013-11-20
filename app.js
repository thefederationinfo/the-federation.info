var express = require('express'),
    mysql = require('mysql'),
    https = require('https'),
    config = require('./config.js');
var app = express();

app.use(express.bodyParser());

app.get('/', function(req, res) {
    res.type('text/plain');
    res.send('diaspora* hub at your service');
});

app.post('/register', function(req, res) {
    console.log(req.ip);
    
    if (! req.body.hasOwnProperty('podhost')) {
        res.statusCode = 400;
        return res.send('Error 400: Post syntax incorrect.');
    }

    var options = {
        host: req.body.podhost,
        port: 443,
        path: '/statistics',
        method: 'GET'
    };
    var request = https.request(options, function(res) {
        console.log('STATUS: ' + res.statusCode);
        console.log('HEADERS: ' + JSON.stringify(res.headers));
        res.setEncoding('utf8');
        res.on('data', function (chunk) {
           console.log('BODY: ' + chunk);
        });
    });
    request.end();
    request.on('error', function(e) {
        console.error(e);
    });
    
    res.type('text/plain');
    res.send('register received');
});

app.listen(process.env.PORT || 4730);
