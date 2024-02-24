var site = new Site();
let menu = [{ innerText: "Главная", href: "./index.html" },
{ innerText: "Курс 1", href: "./Курс 1/index.html" },
{ innerText: "Курс 2", href: "./Курс 2/index.html" },
{ innerText: "Курс 3", href: "./Курс 3/index.html" },
{ innerText: "Курс 4", href: "./Курс 4/index.html" }];
site.add_navigation("Глобальное меню", menu);