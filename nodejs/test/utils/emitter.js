var dts_test = require('dattss').process('test');
var dts_cache = require('dattss').process('cache');


setInterval(function() {
  var min = 10;
  var max = 1500;
  var v = Math.floor(Math.random() * (max - min + 1)) + min;
  dts_test.agg('view', v+'ms');
}, 10);

setInterval(function() {
  var min = 150;
  var max = 2500;
  var v = Math.floor(Math.random() * (max - min + 1)) + min;
  dts_test.agg('search', v+'ms');
}, 10);

setInterval(function() {
  var min = 0;
  var max = 1;
  var v = Math.floor(Math.random() * (max - min + 1)) + min;
  dts_test.agg('view', v+'c!');
}, 10);

setInterval(function() {
  dts_test.agg('error', '1c');
}, 1000);

setInterval(function() {
  dts_test.agg('rss', process.memoryUsage().rss+'g');
}, 1000);

setInterval(function() {
  var min = 0;
  var max = 10;
  var v = Math.floor(Math.random() * (max - min + 1)) + min;
  dts_test.agg('post', v+'c');
}, 10);

var g = 0;
setInterval(function() {
  var min = -5;
  var max = 5;
  var v = Math.floor(Math.random() * (max - min + 1)) + min;
  g += v;
  dts_test.agg('view', g+'g');
}, 10);


setInterval(function() {
  var min = 0;
  var max = 1;
  var v = Math.floor(Math.random() * (max - min + 1)) + min;
  dts_cache.agg('test', + v+'c');
}, 10);


setInterval(function() {
  var min = 150;
  var max = 2500;
  var v = Math.floor(Math.random() * (max - min + 1)) + min;
  dts_cache.agg('search', v+'ms');
}, 10);
