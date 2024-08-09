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
let divName = document.createElement("p");
divName.setAttribute("id", "name");
divName.innerText = "Студенческий сайт ВШОПФ";
head.appendChild(divName);
let divQuote = document.createElement("p");
divQuote.setAttribute("id", "quote");
head.appendChild(divQuote);
quote("Вот где-то здесь есть какая-то жизнь...");

// Генерация подножья сайта
let foot = document.querySelector("footer > div#foot");
let footText = document.createElement("p");
footText.setAttribute("id", "message");
footText.innerHTML = "Будущие поколения ВШОПФа будут благодарны за твой вклад в <a onclick=\"load('https://andromore.github.io/Advanced-School-of-General-and-Applied-Physics/Служебная/Общее дело.html')\">общее дело</a>. ";
footText.innerHTML += "Узнай <a onclick=\"load('https://andromore.github.io/Advanced-School-of-General-and-Applied-Physics/Служебная/Общее дело.html')\">как помочь другим студентам</a> или присылай свои материалы в <a onclick=\"load('https://andromore.github.io/Advanced-School-of-General-and-Applied-Physics/Статьи/Секретные материалы.html')\">секретные материалы</a>.";
foot.appendChild(footText);