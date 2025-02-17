// Глобальное меню
let menu = [{ innerText: "Главная", href: "./index.html" },
    {innerText: "Статьи", href: "./Статьи/index.html"},
{ innerText: "Курс 1", href: "./Курс 1/index.html" },
{ innerText: "Курс 2", href: "./Курс 2/index.html" },
{ innerText: "Курс 3", href: "./Курс 3/index.html" },
{ innerText: "Курс 4", href: "./Курс 4/index.html" }];
let header = document.createElement("header");
let navGlobal = document.createElement("nav");
header.appendChild(navGlobal);
navGlobal.setAttribute("id", "main");
for (i of menu) {
    let a = document.createElement("a");
    a.innerText = i.innerText;
    a.setAttribute("onclick", "load('" + i.href + "')");
    navGlobal.appendChild(a);
}
let divBody = document.getElementsByTagName("header")[0].nextSibling.nextSibling;
document.body.insertBefore(header, divBody);

// Генерация шапки сайта
let head = document.querySelector("header > div#head");
head.setAttribute("class", "row");
let img = document.createElement("img");
img.setAttribute("src", "./logo.png");
img.setAttribute("id", "logo");
head.appendChild(img);
let tmp = document.createElement("div");
tmp.setAttribute("class", "column");
head.append(tmp);
let divName = document.createElement("p");
divName.setAttribute("id", "name");
divName.innerText = "Студенческий сайт ВШОПФ";
tmp.appendChild(divName);
let divQuote = document.createElement("blockquote");
divQuote.innerText = "Вот где-то здесь есть какая-то жизнь...";
divQuote.setAttribute("id", "quote");
tmp.appendChild(divQuote);

// Генерация подножья сайта
let foot = document.querySelector("footer > div#foot");
let footText = document.createElement("p");
footText.setAttribute("id", "message");
footText.innerHTML = "Будущие поколения ВШОПФа будут благодарны за твой вклад в <a onclick=\"load('./Служебная/Общее дело.html')\">общее дело</a>. ";
footText.innerHTML += "Узнай <a onclick=\"load('./Служебная/Общее дело.html')\">как помочь другим студентам</a> или присылай свои материалы в <a onclick=\"load('./Статьи/Секретные материалы.html')\">секретные материалы</a>.";
foot.appendChild(footText);