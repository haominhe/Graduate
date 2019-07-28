'use strict';

var express = require('express');
var bodyParser = require('body-parser');
var fs = require('fs');

var serverPort = 8080;
var server = express();

var guestList = {};

server.use(bodyParser.json());
server.post('/register', function (req, res) {
    Object.keys(req.body).forEach((key) => {
        //assume each family lead doesn't have same email address
        guestList[key] = req.body[key];
    });

    // write guests information into file 'guests.json'
    fs.writeFile('./guests.json', JSON.stringify(guestList), (err) => {
        if (err) console.log(err);
        console.log('The file has been saved!');
    });

    console.log(guestList);
    res.status(200);
    res.set({ 'Content-Type': 'text/plain' });

    res.end();
});

server.get('/registered', function (req, res) {
    res.status(200);
    res.set({ 'Content-Type': 'application/json' });
    res.write(JSON.stringify(guestList));
    res.end();
});

function load_guests() {
    // read guests information from file 'guests.json'
    fs.readFile('./guests.json', function (err, data) {
        if (err) {
            console.log(err);
        } else {
            guestList = JSON.parse(data);
        }
    });
}

load_guests();
server.listen(serverPort);