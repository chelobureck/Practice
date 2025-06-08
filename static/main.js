// Плавное появление элементов
window.addEventListener('DOMContentLoaded', () => {
    setTimeout(() => {
        document.getElementById('main-title').classList.add('show');
    }, 300);
    setTimeout(() => {
        document.getElementById('main-desc').classList.add('show');
    }, 700);
});

// JS-анимация смены текста
const btn = document.getElementById('changeBtn');
const title = document.getElementById('main-title');
const desc = document.getElementById('main-desc');
let toggled = false;
btn.addEventListener('click', () => {
    title.classList.remove('show');
    desc.classList.remove('show');
    setTimeout(() => {
        if (!toggled) {
            title.textContent = 'Добро пожаловать!';
            desc.textContent = 'Это современная и анимированная страница для вашего проекта.';
        } else {
            title.textContent = 'Welcome to the Home Page';
            desc.textContent = 'This is a simple HTML page.';
        }
        title.classList.add('show');
        desc.classList.add('show');
        toggled = !toggled;
    }, 400);
});