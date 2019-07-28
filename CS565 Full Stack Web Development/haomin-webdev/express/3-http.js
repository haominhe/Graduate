'use strict';

var express = require('express'); // do not change this line

// http://localhost:8080/missing should return a status code 404 with 'your princess is in another castle' in plain text

// http://localhost:8080/redirect should redirect the request to '/redirected' by using 302 as the status code

// http://localhost:8080/cache should return 'cache this resource' in plain text and set the cache max age to a day

// http://localhost:8080/cookie should return 'i gave you a cookie' in plain text and set 'hello=world' as a cookie

// http://localhost:8080/check should return 'yes' / 'no' in plain text depending on whether the browser has the 'hello' cookie

var serverPort = process.env.PORT || 8080;
var server = express();

server.get('/missing', function (req, res) {
    res.status(404);
    res.set({ 'Content-Type': 'text/plain' });
    res.write('your princess is in another castle');
    res.end();
})

server.get('/redirect', function (req, res) {
    res.status(302);
    res.set({ 'Location': '/redirected' });
    res.end();
})

server.get('/cache', function (req, res) {
    res.status(200);
    res.set({ 'Content-Type': 'text/plain', 'Cache-Control': 'max-age=86400' });
    res.write('cache this resource');
    res.end();
})

server.get('/cookie', function (req, res) {
    res.status(200);
    res.set({ 'Content-Type': 'text/plain', 'Set-Cookie': 'hello=world' });
    res.write('i gave you a cookie');
    res.end();
})

server.get('/check', function (req, res) {
    const cookie = req.headers.cookie;
    res.status(200);
    res.set({ 'Content-Type': 'text/plain' });
    if (cookie === 'hello=world') {
        res.write('yes');
    } else {
        res.write('no');
    }
    res.end();
})

server.listen(serverPort);




















