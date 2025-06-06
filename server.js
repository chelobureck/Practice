const http = require('http');

let requestCount = 0;

const server = http.createServer((req, res) => {
    requestCount++;

    switch (req.url) {
        case '/':
            res.write('Главная страница');
            break;
        case '/about':
            res.write('О нас');
            break;
        case '/contact':
            res.write('Контакты');
            break;
        default:
            res.write('Страница не найдена');
    }

    res.write('Счтетчик запросов: ' + requestCount);
    res.end();
});

server.listen(3000);