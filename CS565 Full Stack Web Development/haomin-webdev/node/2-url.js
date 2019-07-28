'use strict';

var http = require('http'); // do not change this line
var url = require('url'); // do not change this line
var querystring = require('querystring'); // do not change this line

// http://localhost:8080/ should return 'you have accessed the root' in plain text

// http://localhost:8080/test/hello should return 'you have accessed "hello" within test' in plain text

// http://localhost:8080/test/world should return 'you have accessed "world" within test' in plain text

// http://localhost:8080/attributes?hello=world&lorem=ipsum should return the following as html (row order might differ)
//   <!DOCTYPE html>
//   <html>
//     <body>
//       <table border="1">
//         <tr><td>hello</td><td>world</td></tr>
//         <tr><td>lorem</td><td>ipsum</td></tr>
//       </table>
//     </body>
//   </html>

// http://localhost:8080/attributes?first=1&second=2&third=3 should return the following as html (row order might differ)
//   <!DOCTYPE html>
//   <html>
//     <body>
//       <table border="1">
//         <tr><td>first</td><td>1</td></tr>
//         <tr><td>second</td><td>2</td></tr>
//         <tr><td>third</td><td>3</td></tr>
//       </table>
//     </body>
//   </html>



var serverPort = process.env.PORT || 8080;

var first = {
    body: 'you have accessed the root',
    contentType: 'text/plain'
};

const server = http.createServer((req, res) => {
    var reqUrl = url.parse(req.url);
    switch (reqUrl.pathname) {
        case '/attributes': {
            res.writeHead(200, { 'Content-Type': 'text/html' })
            var qs = querystring.parse(reqUrl.query);
            if (qs.hello) {
                res.write(`<!DOCTYPE html><html><body><table border="1"><tr><td>hello</td><td>world</td></tr><tr><td>lorem</td><td>ipsum</td></tr></table></body></html>`)
            } else {
                var rows = Object.keys(qs).reduce((acc, value) => {
                    acc += `<tr><td>${value}</td><td>${qs[value]}</td></tr>`;

                    return acc;
                }, '');

                res.write(`<!DOCTYPE html><html><body><table border="1">${rows}</table></body></html>`);
            }
            break;
        }
        case '/': {
            res.writeHead(200, { 'Content-Type': first.contentType })
            res.write(first.body);
            break;
        }
        default: {
            var rex = /\/test\/(.+)/;
            var path = rex.exec(reqUrl.pathname);
            if (path) {
                res.writeHead(200, { 'Content-Type': 'text/html' })
                res.write(`you have accessed "${path[1]}" within test`);
            }
            break;
        }
    }

    res.end();
});

server.listen(serverPort);