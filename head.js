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
            quote("Вот где-то здесь есть какая-то жизнь...");
            scripts = tmp.querySelectorAll("body script:not(main script)");
            for (i of scripts) {
                script = document.createElement("script");
                if (i.hasAttribute("src")) {
                    if (i.getAttribute("src").indexOf("body.js") == -1 && i.getAttribute("src").indexOf("head.js") == -1) {
                        script.setAttribute("src", i.getAttribute("src"));
                    }
                    else continue;
                }
                script.innerHTML = i.innerHTML;
                document.body.appendChild(script);
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