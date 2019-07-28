'use strict';

var express = require('express'); // do not change this line
var socket = require('socket.io'); // do not change this line
var assert = require('assert'); // do not change this line

var server = express();

server.use('/', express.static(__dirname + '/'));

var io = socket(server.listen(process.env.PORT || 8080)); // do not change this line

var clients = [];

io.on('connection', function (objectSocket) {
	clients.push(objectSocket.id);

	clients.forEach((client)=> {
		objectSocket.to(client).emit('clients', { strClients: clients });
	});

	objectSocket.emit('clients', { strClients: clients });

	var message = objectSocket.id + ' connected';
	clients.forEach((client)=> {
		objectSocket.to(client).emit('message', { 'strFrom': 'server', 'strTo': 'everyone', 'strMessage': message })
	});
	objectSocket.emit('message', { 'strFrom': 'server', 'strTo': 'everyone', 'strMessage': message })

	// send everyone the 'clients' event, contianing an array with the ids of the connected clients - example: { 'strClients':['GxwYr9Uz...','9T1P4pUQ...'] }
	// send everyone the 'message' event, containing a message that a new client connected - example: { 'strFrom':'server', 'strTo':'everyone', 'strMessage':'9T1P4pUQ... connected' }

	objectSocket.on('message', function (objectData) {
		if (objectData.strTo === 'everyone') {
			clients.forEach((client)=> {
				objectSocket.to(client).emit('message', { 'strFrom': objectSocket.id, 'strTo': 'everyone', 'strMessage':  objectData.strMessage })
			});
		} else {
			objectSocket.to(objectData.strTo).emit('message', { 'strFrom': objectSocket.id, 'strTo': objectData.strTo, 'strMessage': objectData.strMessage })
		}
		objectSocket.emit('message', { 'strFrom': objectSocket.id, 'strTo': objectData.strTo, 'strMessage': objectData.strMessage })

		// if the message should be recevied by everyone, broadcast it accordingly
		// if the message has a single target, send it to this target as well as to the origin
	});

	objectSocket.on('disconnect', function () {
		var index = clients.indexOf(objectSocket.id);
		clients.splice(index, 1);

		clients.forEach((client)=> {
			objectSocket.to(client).emit('clients', { strClients: clients });

			var discMessage = objectSocket.id +' disconnected';
			objectSocket.to(client).emit('message', { 'strFrom': 'server', 'strTo': 'everyone', 'strMessage': discMessage })
		});

		// send everyone the 'clients' event, contianing an array of the connected clients - example: { 'strClients':['GxwYr9Uz...'] }
		// send everyone the 'message' event, containing a message that an existing client disconnected - example: { 'strFrom':'server', 'strTo':'everyone', 'strMessage':'9T1P4pUQ... disconnected' }
	});
});

console.log('go ahead and open "http://localhost:8080/3-chat.html" in your browser');