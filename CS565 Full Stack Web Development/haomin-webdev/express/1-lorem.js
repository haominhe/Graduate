'use strict';

var express = require('express'); // do not change this line

// http://localhost:8080/lorem should return '<!DOCTYPE html><html><body>lorem ipsum</body></html>' as html

var serverPort = process.env.PORT || 8080;
var server = express();

server.get('/lorem', function(req, res){
    res.status(200);
    res.set({ 'Content-Type': 'text/html' })
    res.write('<!DOCTYPE html><html><body>lorem ipsum</body></html>');
    res.end();
})

server.listen(serverPort);