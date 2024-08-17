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
    try {
        if (push) window.history.pushState({ url: filename }, null, filename);
    }
    catch {
        // Сыпется в локальной версии
    }
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
    // Делать было нечего - делать было нечего
    /*
    Инструкция сломается только при выполнении локальных скриптов
    (при отладке локальной версии в браузере - в рабочей версии всё будет нормально)
    И на рабочую версию не повлияет
    */
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