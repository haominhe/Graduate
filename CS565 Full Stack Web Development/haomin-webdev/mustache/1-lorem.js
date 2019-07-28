var express = require('express');
var mustache = require('mustache');
var fs = require('fs');

var server = express();

server.get('/1-lorem.html', function (req, res) {
	fs.readFile('./1-lorem.html', function (err, data) {
		res.writeHead(200, {
			'Content-Type': 'text/html'
		});

		res.write(mustache.render(data.toString(), {
			'objectUser': {
				'strFirst': 'max',
				'strLast': 'mustermann'
			},
			'strMessage': 'hello world'
		}));

		res.end();
	});
});

server.listen(8080);

console.log('go ahead and open "http://localhost:8080/1-lorem.html" in your browser');



// hello max mustermann, our message of today is: "hello world"