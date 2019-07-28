'use strict';

var express = require('express'); // do not change this line
var parser = require('body-parser'); // do not change this line

// preface: use the body-parser middleware that helps you retrieve and parse the post data from the form

// http://localhost:8080/form should return the form as shown below
//   res.status(200);
//   
//   res.set({
//   	'Content-Type': 'text/html'
//   });
//   
//   res.write('<!DOCTYPE html>');
//   res.write('<html>');
//   	res.write('<body>');
//   		res.write('<form action="/new" method="post">');
//   			res.write('<input type="text" name="name">');
//   			res.write('<input type="text" name="message">');
//   			res.write('<input type="submit" value="submit">');
//   		res.write('</form>');
//   	res.write('</body>');
//   res.write('</html>');
//   
//   res.end();

// http://localhost:8080/new should retrieve the post data, save the name / message (in a global variable) and return 'thank you for your message' in plain text

// http://localhost:8080/list should return the stored messages (from the global variable) 'name: message' in plain text

// http://localhost:8080/form should return the form as shown aboe

// http://localhost:8080/new should retrieve the post data using the body parser, save the name / message (in a global variable) and return 'thank you for your message' in plain text

// http://localhost:8080/list should return the stored messages (from the global variable) 'name: message\nanother name: another message' in plain text

// [the server restarts and looses all messages]

// http://localhost:8080/list should return '' in plain text


var serverPort = process.env.PORT || 8080;
var server = express();
var whole = '';
var posttext;

server.get('/form', function (req, res) {
    res.status(200);
    res.set({ 'Content-Type': 'text/html' });
    res.write('<!DOCTYPE html>');
    res.write('<html>');
    res.write('<body>');
    res.write('<form action="/new" method="post">');
    res.write('<input type="text" name="name">');
    res.write('<input type="text" name="message">');
    res.write('<input type="submit" value="submit">');
    res.write('</form>');
    res.write('</body>');
    res.write('</html>');

    res.end();
})

server.post('/new', function (req, res) {
    res.status(200);
    res.set({ 'Content-Type': 'text/plain' });
    res.write('thank you for your message');

    if (req.method == 'POST') {
        //console.log(whole);
        req.on('data', function (data) {
            whole += data;
            if (whole.length > 1e6) {
                req.connection.destroy();
            }
        });
        req.on('end', function () {
            // console.log(whole);
            //posttext = querystring.parse(whole);
            // console.log(posttext);
        });
    }

    res.end();
})

server.get('/list', function (req, res) {
    res.status(200);
    res.set({ 'Content-Type': 'text/plain' });
    if (whole === '') {
        res.write('');
        res.end();
    }

    console.log(whole);
    //console.log(posttext);
    var params = {}, queries, temp, i, l;
    queries = whole.split("&").join(',').split('=').join(',').split('name').join(',').split('message').join('').split(',').filter(String);


    for (i = 0, l = queries.length; i < l; i = i + 2) {
        // console.log(queries);
        console.log(queries[l - 1]);
        if (i !== l - 2) {
            res.write(`${queries[i]}: ${queries[i + 1]}\n`)
        } else {
            res.write(`${queries[i]}: ${queries[i + 1]}`)
        }
    }
    res.end();
})

server.listen(serverPort);

