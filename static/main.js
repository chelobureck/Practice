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

fetch('/gpt', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({history: chatHistory})
})
.then(res => res.json())
.then(data => {
    if (data.error) {
        showError(data.error);
    } else {
        renderSlides(data.images);
        // Сохраняем id презентации для скачивания
        window.currentPresentationId = data.presentation_id;
        document.getElementById('pptx-download-btn').onclick = function() {
            window.location.href = '/download_pptx/' + window.currentPresentationId;
        };
    }
});

function showError(msg) {
    alert(msg); // или красивый блок на странице
}

function renderSlides(images) {
    const preview = document.getElementById('pptx-preview');
    preview.innerHTML = '';
    images.forEach(img => {
        const imageElem = document.createElement('img');
        imageElem.src = img;
        imageElem.style = "max-width:90vw;display:block;margin:20px auto;";
        preview.appendChild(imageElem);
    });
    preview.style.display = 'block';
    document.getElementById('pptx-download-btn').style.display = 'block';
}