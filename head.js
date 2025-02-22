// Константы (в данном случае ссылки)
const BaseURL = "https://andromore.github.io/Advanced-School-of-General-and-Applied-Physics/";
const StartURL = window.location.href;

// Новый загрузчик страниц
function load(filename, push = true) {
    // Приведение ссылок к единому виду - абсолютная ссылка на веб-ресурс
    if (filename.slice(0, 2) == "./")
        filename = filename.replace("./", BaseURL);
    else if (filename.slice(0, BaseURL.length) != BaseURL)
        throw Error("Wrong filename '" + filename + "' - I can't load it.");
    // Запрос веб-ресурса
    let xhr = new XMLHttpRequest();
    xhr.overrideMimeType("text/html");
    xhr.open('GET', filename, true);
    xhr.onload = function () {
        // Обработка результата запроса (200 - "всё хорошо", иначе обрабатываем ошибку)
        if (xhr.status === 200) {
            // Очищаем принимающую страницу
            let main = document.getElementsByTagName("main")[0];
            main.innerHTML = "";
            // Обрабатываем содержимое загружаемой страницы
            let tmp = document.createElement("div");
            tmp.innerHTML = xhr.response; // Получаем содержимое всей загружаемой страница
            container = tmp.getElementsByTagName("main")[0]; // Нужен только её контент
            // Обрабатываем ссылки
            for (a of container.getElementsByTagName("a")) {
                if (a.hasAttribute("href")) {
                    a.setAttribute("href", a.getAttribute("href").replace("./", BaseURL));
                }
            }
            // Обрабатываем изображения
            for (img of container.getElementsByTagName("img")) {
                if (img.hasAttribute("src")) {
                    img.setAttribute("src", img.getAttribute("src").replace("./", BaseURL));
                }
            }
            // Перенос всех элементов дотошным копированием (чтобы работали скрипты)
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
            // База страницы должна быть единой и не должна отличаться от базы страницы, на которой вызывается метод
            if (main.getElementsByTagName('base')[0]) {
                main.removeChild(main.getElementsByTagName('base')[0]);
            }
            // Добавление посещения в историю
            try {
                if (push) window.history.pushState({ url: filename }, null, filename);
            }
            catch {
                // В локальной версии не работает управление историей
                // alert("Ошибка при управлении историей посещений сайта (требуется ввиду динамической загрузки страниц). Если ошибка произошла не в локальной версии, просьба перейти на страницу \"Служебные\" > \"Ошибка\" и сообщить о произошедшем.");
            }
        } else {
            // Вызывается страница ошибки
            load(BaseURL + "Служебная/Ошибка.html");
        }
    }
    xhr.send(null);
}

// Обработчик событий истории
window.addEventListener("popstate", (event) => {
    if (event.state.url)
        load(event.state.url, false);
    else {
        // Если что-то пошло не так - загружаемся в начало (возможно редуцент)
        console.log("Возвращаемся на начальную страницу - ошибка возвращения по истории");
        load(StartURL, false);
    }
});

// Изменение state начальной страницы
try {
    window.history.replaceState({ url: StartURL }, null, StartURL);
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