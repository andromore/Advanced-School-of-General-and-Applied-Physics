const BaseURL = "https://andromore.github.io/Advanced-School-of-General-and-Applied-Physics/index.html";

// Новый загрузчик страниц
function load(filename, push = true) {
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
            for (a of container.getElementsByTagName("a")) {
                if (a.hasAttribute("href")) {
                    a.setAttribute("href", a.getAttribute("href").replace("./", "https://andromore.github.io/Advanced-School-of-General-and-Applied-Physics/"));
                }
            }
            for (img of container.getElementsByTagName("img")) {
                if (img.hasAttribute("src")) {
                    img.setAttribute("src", img.getAttribute("src").replace("./", "https://andromore.github.io/Advanced-School-of-General-and-Applied-Physics/"));
                }
            }
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
            try {
                if (push) window.history.pushState({ url: filename }, null, filename);
            }
            catch {
                alert("Ошибка при управлении историей посещений сайта (требуется ввиду динамической загрузки страниц). Если ошибка произошла не в локальной версии, просьба перейти на страницу \"Служебные\" > \"Ошибка\" и сообщить о произошедшем.");
            }
        } else {
            load("https://andromore.github.io/Advanced-School-of-General-and-Applied-Physics/Служебная/Ошибка.html");
        }
    }
    xhr.send(null);
}

// Обработчик событий
window.addEventListener("popstate", (event) => {
    if (event.state.url)
        load(event.state.url, false);
    else {
        load(BaseURL, false);
    }
});

// Изменение state начальной страницы
try {
    window.history.replaceState({ url: BaseURL }, null, BaseURL);
}
catch {
    alert("Ошибка при попытке изменения базового URL (требуется ввиду динамической загрузки страниц). Если ошибка произошла не в локальной версии, просьба перейти на страницу \"Служебные\" > \"Ошибка\" и сообщить о произошедшем.");
}

// Заголовок сайта
let title = document.createElement("title");
title.textContent = "ВШОПФ";
document.head.appendChild(title);

// Иконка
let icon = document.createElement("link");
icon.setAttribute("rel", "icon");
icon.setAttribute("href", "./logo.ico");
document.head.appendChild(icon);

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

// VK Open API
let script = document.createElement("script");
script.setAttribute("type", "text/javascript");
script.setAttribute("src", "https://vk.com/js/api/openapi.js?168");
script.setAttribute("charset", "windows-1251");
document.head.appendChild(script);

// Описание страницы
meta = document.createElement("meta");
meta.setAttribute("name", "description");
meta.setAttribute("content", "Студенческий сайт ВШОПФ - Высшей Школы Общей и Прикладной Физики - базового факультета Института Прикладной Физики РАН");
document.head.appendChild(meta);

// Поисковые роботы
meta = document.createElement("meta");
meta.setAttribute("name", "robots");
meta.setAttribute("content", "all");
document.head.appendChild(meta);

// Ключевые слова
meta = document.createElement("meta");
meta.setAttribute("name", "keywords");
meta.setAttribute("content", "ВШОПФ, Высшая Школа Общей и Прикладной Физики, ИПФ РАН, Институт Прикладной Физики Российской Академии Наук");
document.head.appendChild(meta);