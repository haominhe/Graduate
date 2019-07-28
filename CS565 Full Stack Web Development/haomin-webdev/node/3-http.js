'use strict';

var http = require('http'); // do not change this line

// http://localhost:8080/missing should return a status code 404 with 'your princess is in another castle' in plain text

// http://localhost:8080/redirect should redirect the request to '/redirected' by using 302 as the status code

// http://localhost:8080/cache should return 'cache this resource' in plain text and set the cache max age to a day

// http://localhost:8080/cookie should return 'i gave you a cookie' in plain text and set 'hello=world' as a cookie

// http://localhost:8080/check should return 'yes' / 'no' in plain text depending on whether the browser has the 'hello' cookie


const serverPort = process.env.PORT || 8080;

const server = http.createServer((req, res) => {
    // console.log(req);
    //request url 
    switch (req.url) {
        case '/missing': {
            res.writeHead(404, { 'Content-Type': 'text/plain' });
            res.write('your princess is in another castle');
            break;
        }
        case '/redirect': {
            res.writeHead(302, { 'Location': '/redirected' });
            break;
        }
        case '/cache': {
            res.writeHead(200, { 'Content-Type': 'text/plain', 'Cache-Control': 'max-age=86400' });
            res.write('cache this resource');
            break;
        }
        case '/cookie': {
            res.writeHead(200, { 'Content-Type': 'text/plain', 'Set-Cookie': 'hello=world' });
            res.write('i gave you a cookie');
            break;
        }
        case '/check': {
            const cookie = req.headers.cookie;
            console.log(cookie)
            res.writeHead(200, { 'Content-Type': 'text/plain' });

            if (cookie === 'hello=world') {
                 res.write('yes');

            }else {
                res.write('no');

            }
            break;
        }
    }
    res.end();
});

server.listen(serverPort);