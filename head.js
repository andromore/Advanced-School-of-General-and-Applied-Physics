// Цитата на странице
function quote(text) {
    document.getElementById('quote').innerText = text;
}

// Новый загрузчик страниц
function load(filename) {
    let xhr = new XMLHttpRequest();
    xhr.overrideMimeType("text/html");
    xhr.open('GET', filename, true);
    xhr.onload = function () {
        if (xhr.status === 200) {
            let main = document.getElementsByTagName("main")[0];
            main.innerHTML = "";
            let tmp = document.createElement("div");
            tmp.innerHTML = xhr.response;
            container = tmp.getElementsByTagName("main")[0];
            for (i of container.childNodes) {
                if (i.nodeType == 1) {
                    main.appendChild(i.cloneNode(true));
                }
            }
            if (main.getElementsByTagName('base')[0]) {
                main.removeChild(main.getElementsByTagName('base')[0]);
            }
        } else {
            console.error('Сетевая ошибка, сообщим голубям!');
        }
    }
    xhr.send(null);
    window.history.pushState({url: filename}, null, filename);
}

window.addEventListener("popstate", (event) => {  
    load(event.state.url);
});

// Заголовок сайта
let title = document.createElement("title");
title.textContent = "ВШОПФ";
document.head.appendChild(title);

// Кодировка
let meta = document.createElement("meta");
meta.setAttribute("charset", "utf-8");
document.head.appendChild(meta);

// Для работы адаптивного дизайна с разными размерами отображаемого пространства
meta = document.createElement("meta");
meta.setAttribute("name", "viewport");
meta.setAttribute("content", "width=device-width");
document.head.appendChild(meta);

// Загрузка темы
let stylesheet = document.createElement("link");
stylesheet.setAttribute("href", "./theme.css");
stylesheet.setAttribute("rel", "stylesheet");
document.head.appendChild(stylesheet);