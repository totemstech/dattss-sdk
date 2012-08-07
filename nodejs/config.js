var fwk = require('fwk');
var config = fwk.baseConfig();

config['DATTSS_PUSH_PERIOD'] = 5 * 1000;
config['DATTSS_PERCENTILE'] = 0.1;

config['DATTSS_AUTH_KEY'] = 'DUMMY';
config['DATTSS_SERVER_HTTP_HOST'] = 'agg.dattss.com';
config['DATTSS_SERVER_HTTP_PORT'] = 80;
config['DATTSS_SERVER_UDP_HOST'] = 'udp.dattss.com';
config['DATTSS_SERVER_UDP_PORT'] = 8125;

config['DATTSS_DRIVER_DEBUG'] = false;

exports.config = config;
