const http = require('http');

let requestCount = 0;

const server = http.createServer((req, res) => {
    requestCount++;

    switch (req.url) {
        case '/':
            res.write('Welcome to the home page!');
            res.write('response: ' + requestCount);
            break;
        case '/about':
            res.write('This is the about page.');
            break;      
        case '/contact':    
            res.write('Contact us at');
            break;
        default:
            res.write('DOLBAEB TAKOGO SAYTA NETU');
            break;
    }
    res.end();
});

server.listen(3000);