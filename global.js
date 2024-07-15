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

// Глобальное меню
let menu = [{ innerText: "Главная", href: "https://andromore.github.io/Advanced-School-of-General-and-Applied-Physics/index.html" },
    {innerText: "Статьи", href: "https://andromore.github.io/Advanced-School-of-General-and-Applied-Physics/Статьи/index.html"},
{ innerText: "Курс 1", href: "https://andromore.github.io/Advanced-School-of-General-and-Applied-Physics/Курс 1/index.html" },
{ innerText: "Курс 2", href: "https://andromore.github.io/Advanced-School-of-General-and-Applied-Physics/Курс 2/index.html" },
{ innerText: "Курс 3", href: "https://andromore.github.io/Advanced-School-of-General-and-Applied-Physics/Курс 3/index.html" },
{ innerText: "Курс 4", href: "https://andromore.github.io/Advanced-School-of-General-and-Applied-Physics/Курс 4/index.html" }];
let header = document.createElement("header");
let navGlobal = document.createElement("nav");
header.appendChild(navGlobal);
navGlobal.setAttribute("class", "structure");
navGlobal.setAttribute("id", "main");
for (i of menu) {
    let a = document.createElement("a");
    a.innerText = i.innerText;
    a.setAttribute("onclick", 'load("' + i.href + '")');
    navGlobal.appendChild(a);
}
let divBody = document.getElementsByTagName("header")[0].nextSibling.nextSibling;
document.body.insertBefore(header, divBody);

// Генерация шапки сайта
let head = document.querySelector("header > div#head");
let divName = document.createElement("div");
divName.setAttribute("id", "name");
divName.innerText = "Студенческий сайт ВШОПФ";
head.appendChild(divName);
let divQuote = document.createElement("div");
divQuote.setAttribute("id", "quote");
divQuote.innerText = "Вот где-то здесь есть какая-то жизнь...";
head.appendChild(divQuote);

// Генерация подножья сайта
let foot = document.querySelector("footer > div#foot");
let footText = document.createElement("div");
footText.setAttribute("id", "message");
footText.innerHTML = "Будущие поколения ВШОПФа будут благодарны за твой вклад в <a onclick=\"load('https://andromore.github.io/Advanced-School-of-General-and-Applied-Physics/Служебная/Общее дело.html')\">общее дело</a>. ";
footText.innerHTML += "Узнай <a onclick=\"load('https://andromore.github.io/Advanced-School-of-General-and-Applied-Physics/Служебная/Общее дело.html')\">как помочь другим студентам</a> или присылай свои материалы в <a onclick=\"load('https://andromore.github.io/Advanced-School-of-General-and-Applied-Physics/Статьи/Секретные материалы.html')\">секретные материалы</a>.";
foot.appendChild(footText);

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
                    tmp = document.createElement(i.nodeName);
                    for (j in i) {
                        if (i.getAttribute(j)) {
                            tmp.setAttribute(j, i.getAttribute(j));
                        }
                    }
                    tmp.innerHTML = i.innerHTML;
                    tmp.className = i.className;
                    main.appendChild(tmp);
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
}

// Цитата на странице
function quote(text) {
    document.getElementById('quote').innerText = text;
}