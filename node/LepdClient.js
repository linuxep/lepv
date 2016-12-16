var rpc = require('node-json-rpc');

var options = {
    // int port of rpc server, default 5080 for http or 5433 for https 
    port: 12307,
    // string domain name or ip of rpc server, default '127.0.0.1' 
    host: 'www.readeeper.com',
    // string with default path, default '/' 
    path: '/',
    // boolean false to turn rpc checks off, default true 
    strict: true
};

// Create a server object with options 
var client = new rpc.Client(options);

//echo "{\"method\":\"GetCmdDf\"}" | nc localhost 12307
client.call(
    {"method": "GetCmdDf"},
    function (err, res) {
        // Did it all work ? 
        if (err) { 
            console.log(err);
        }
        else {
            console.log(res);
        }
    }
);

//client.call(
//    {"method": "GetCmdDf"},
//    function (err, res) {
//        // Did it all work ? 
//        if (err) { console.log(err); }
//        else { console.log(res); }
//    }
//);