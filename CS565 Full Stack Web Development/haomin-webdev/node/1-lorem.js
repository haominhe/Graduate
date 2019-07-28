'use strict';

var http = require('http'); // do not change this line

// any request should return '<!DOCTYPE html><html><body>lorem ipsum</body></html>' as html
var serverPort = process.env.PORT || 8080;

var html = '<!DOCTYPE html><html><body>lorem ipsum</body></html>';

const server = http.createServer((req, res) => {
    res.writeHead(200, { 'Content-Type': 'text/html' })
    res.write(html);
    res.end();
});

server.listen(serverPort);