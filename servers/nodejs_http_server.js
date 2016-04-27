var http = require('http');


const PORT = 25000;


function handle(request, response) {
    var msize = request.url.substr(1);
    if (!msize) {
        msize = 1024;
    } else {
        msize = parseInt(msize);
    }
    response.end(Array(msize).join("X"));
}


var server = http.createServer(handle);

server.listen(PORT, function() {});
