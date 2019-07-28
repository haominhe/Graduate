
'use strict';

var http = require('http');// do not change this line
var dns = require('dns');// do not change this line

// http://localhost:8080/pdx.edu should return '131.252.115.150' in plain text (address might be different, there could even be multiple addresses)

// http://localhost:8080/sniklaus.com should return '216.239.36.21\n216.239.38.21\n216.239.32.21\n216.239.34.21' in plain text (addresses / order might be different)

// http://localhost:8080/error should return 'error' in plain text

const serverPort = process.env.PORT || 8080;

function getIp(sec, callback) {
    // dns resolve is an asyncronous method, have to wait for it to come back. 
    dns.resolve4(sec, (err, address) => {
        if (err) {
            console.log(' error: ' + err.message);
            callback('error');
        } else {
            callback(null, address);
        }
    });
}


const server =
    http.createServer((req, res) => {
        var thisstr = req.url;
        res.writeHead(200, { 'Content-Type': 'text/plain' });
        if (thisstr === '/favico.ico') {
            res.end();
        }
        if (thisstr === '/error') {
            res.writeHead(200, { 'Content-Type': 'text/plain' });
            res.write('error');
            res.end();
            return
        }
        const lst = thisstr.substr(thisstr.indexOf('\\') + 1);
        const sec = lst.substr(1);
        getIp(sec, (err, address) => {
            if (err) {
                res.write(err);
            } else {
                const ipString = address.join('\n');
                res.writeHead(200, { 'Content-Type': 'text/plain' });
                res.write(ipString);
            }
            res.end();
        });
    });

server.listen(serverPort);