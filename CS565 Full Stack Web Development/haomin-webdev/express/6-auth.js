'use strict';

var express = require('express'); // do not change this line
var passport = require('passport'); // do not change this line
var Strategy = require('passport-http').BasicStrategy; // do not change this line

// preface: use the passport middleware and only grant the user "test" with the password "logmein" access

// note: should the server restart, the browser will still technically be logged in since we are using the http basic access authentication which lets the browser submit the username and the password at each request

// http://localhost:8080/hello should return 'accessible to everyone' in plain text

// http://localhost:8080/world should return 'only accessible when logged in' in plain text if user the user is authenticate, otherwise will prompt for the username and password

// http://localhost:8080/test should return 'only accessible when logged in' in plain text if user the user is authenticate, otherwise will prompt for the username and password

var user = {
    username: 'test',
    password: 'logmein'
}

var serverPort = process.env.PORT || 8080;
var server = express();
server.use(passport.initialize());
server.use(passport.session());
passport.serializeUser(function (user, done) {
    done(null, user);
});

passport.deserializeUser(function (user, done) {
    done(null, user);
});

passport.use(new Strategy(
    function (username, password, cb) {
        if (!username) { return cb(null, false); }
        if (username != user.username || password != user.password) { return cb(null, false); }
        return cb(null, {});
    }
));

server.get('/hello', function (req, res) {
    res.status(200);
    res.set({ 'Content-Type': 'text/plain' });
    res.write('accessible to everyone');
    res.end();
})

server.get('/world', passport.authenticate('basic'), function (req, res) {
    res.status(200);
    res.set({ 'Content-Type': 'text/plain' });
    res.write('only accessible when logged in');
    res.end();
})

server.get('/test',  passport.authenticate('basic'), function (req, res) {
    res.status(200);
    res.set({ 'Content-Type': 'text/plain' });
    res.write('only accessible when logged in');
    res.end();
})

server.listen(serverPort);





















