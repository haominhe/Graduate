'use strict';

var http = require('http'); // do not change this line

// http://localhost:8080/hello should return 'you must be new' in plain text and set an ident cookie

// http://localhost:8080/test should return 'last time you visited "/hello"' in plain text

// http://localhost:8080/world should return 'last time you visited "/test"' in plain text

// [now sending requests from a different browser]

// http://localhost:8080/lorem should return 'you must be new' in plain text and set an ident cookie

// http://localhost:8080/moshimoshi should return 'last time you visited "/lorem"' in plain text

// http://localhost:8080/ipsum should return 'last time you visited "/moshimoshi"' in plain text

// [sending requests from the original browser again]

// http://localhost:8080/again should return 'last time you visited "/world"' in plain text

// [the server restarts and looses all cookies]

// http://localhost:8080/servus should return 'you must be new' in plain text and set an ident cookie

const serverPort = process.env.PORT || 8080;

const server = http.createServer((req, res) => {
    const cookie = req.headers.cookie;

    if (!cookie) {
        res.writeHead(200, { 'Content-Type': 'text/plain', 'Set-Cookie': `hello=${req.url}` });
        res.write('you must be new');
    } else {
        res.writeHead(200, { 'Content-Type': 'text/plain', 'Set-Cookie': `hello=${req.url}` });
        const rex = /hello\=(.+)/.exec(cookie);
        const path = rex[1];
        res.write(`last time you visited "${path}"`);
    }

    res.end();
});

server.listen(serverPort);