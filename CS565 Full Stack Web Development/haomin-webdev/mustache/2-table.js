var express = require('express');
var mustache = require('mustache');
var fs = require('fs');

var server = express();

server.get('/2-table.html', function (req, res) {
	fs.readFile('./2-table.html', function (err, data) {
		res.writeHead(200, {
			'Content-Type': 'text/html'
		});

		res.write(mustache.render(data.toString(), {
			'objectUsers': [
				{ 'strFirst': 'max', 'strLast': 'baum', 'strGender': 'male', 'boolVisible': true },
				{ 'strFirst': 'anna', 'strLast': 'hahn', 'strGender': 'female', 'boolVisible': true },
				{ 'strFirst': 'tim', 'strLast': 'stein', 'strGender': 'male', 'boolVisible': true }
			],
			'functionName': function () {
				return this.strFirst + ' ' + this.strLast;
			}
		}));

		res.end();
	});
});

server.listen(8080);

console.log('go ahead and open "http://localhost:8080/2-table.html" in your browser');