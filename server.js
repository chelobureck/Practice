const http = require('http');
const fs = require('fs');

const delay = (ms) => new Promise((resolve, reject) => {
    setTimeout(() => {
        resolve();
    }, ms);
}); // Функция задержки

const readFileAsync = (filePath) => new Promise((resolve, reject) => {
    fs.readFile(filePath, (err, data) => {
        if (err) reject(err);
        else resolve(data);
    });
}); // Чтение файла асинхронно

const server = http.createServer(async (req, res) => {
    switch (req.url) {
        case '/':
            // Главная страница в файле index.html
            try {
                const data = await readFileAsync('index.html');  
                res.write(data);
                res.end();
                break;
            } catch (err) {
                res.write('Internal Server Error');
                res.end();
            }
        case '/about':
            await delay(3000);
            res.write('This is the about page.');
            res.end();
            break;      
        case '/contact':    
            res.write('Contact us at');
            res.end();
            break;
        default:
            // Обработка 404 ошибки
            res.write('404 Not Found');
            res.end();
            break;
    }
});

server.listen(3000); // Запуск сервера на порту 3000