var express = require('express');
var mustache = require('mustache');
var fs = require('fs');

var server = express();

server.get('/3-logic.html', function (req, res) {
	fs.readFile('./3-logic.html', function (err, data) {
		res.writeHead(200, {
			'Content-Type': 'text/html'
		});

		res.write(mustache.render(data.toString(), {
			'objectStocks': [
				{ 'strName': 'AMD.NAS', 'dblValue': 6.735, 'dblChange': -0.17, 'intTime': 1469635304434, 'intVolume': 19873260 },
				{ 'strName': 'FME.FRA', 'dblValue': 81.41, 'dblChange': 0.25, 'intTime': 1469635495373, 'intVolume': 506131 },
				{ 'strName': 'MSFT.NAS', 'dblValue': 56.34, 'dblChange': -0.43, 'intTime': 1469635411375, 'intVolume': 10467243 }
			]
			// 'date': function () {
			// 	var dateobj = new Date(this.intTime);
			// 	var year, month, day, hour, min, sec, misec;
			// 	year = dateobj.getFullYear();
			// 	month = (dateobj.getMonth() + 1).toString().slice(-2);
			// 	day = dateobj.getDate();
			// 	hour = dateobj.getHours().toString().slice(-2);
			// 	min = dateobj.getMinutes().toString().slice(-2);
			// 	sec = dateobj.getSeconds().toString().slice(-2);
			// 	misec = dateobj.getMilliseconds();
			// 	return `${year}.${month}.${day} - ${hour}:${min}:${sec}.${misec}`
			// },
			// 'volume': function () {
			// 	var units = ['T', 'M', 'B'],
			// 		decimal;
			// 	var num = this.intVolume;
			// 	for (var i = units.length - 1; i >= 0; i--) {
			// 		decimal = Math.pow(1000, i + 1);

			// 		if (num <= -decimal || num >= decimal) {
			// 			return +(num / decimal).toFixed(1) + ' ' + units[i];
			// 		}
			// 	}

			// 	return num;
			// },
			// 'formatnum':function (){
		
			// 	return (Math.floor(100 * this.dblValue) / 100).toFixed(2);
			// }, 
			// 'formatnum2':function (){
			// 	return this.dblChange.toFixed(2);
			// }
		}));

		res.end();
	});
});

server.listen(8080);

console.log('go ahead and open "http://localhost:8080/3-logic.html" in your browser');