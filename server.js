const http = require('http');

let requestCount = 0;

const server = http.createServer((req, res) => {
    requestCount++;
    res.write('Счтетчик запросов: ' + requestCount);
    res.end();
});

server.listen(3000);