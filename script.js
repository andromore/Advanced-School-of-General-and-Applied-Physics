class SiteHeader extends HTMLElement {
    constructor() {
        super();
    }
}

class SiteHead extends HTMLElement {
    constructor() {
        super();
    }
}

class SiteBody extends HTMLElement {
    constructor() {
        super();
    }
}

class SiteMain extends HTMLElement {
    constructor() {
        super();
    }
}

class SiteLeftBar extends HTMLElement {
    constructor() {
        super();
    }
}

class SiteContent extends HTMLElement {
    constructor() {
        super();
    }
}

class SiteRightBar extends HTMLElement {
    constructor() {
        super();
    }
}

class SiteFooter extends HTMLElement {
    constructor() {
        super();
    }
}

class SiteFoot extends HTMLElement {
    constructor() {
        super();
    }
}

class SiteNavigation extends HTMLElement {
    constructor() {
        super();
    }
}

class Site {
    head;

    constructor() {
        customElements.define("site-header", SiteHeader);
        customElements.define("site-head", SiteHead);
        customElements.define("site-body", SiteBody);
        customElements.define("site-main", SiteMain);
        customElements.define("site-left-bar", SiteLeftBar);
        customElements.define("site-content", SiteContent);
        customElements.define("site-right-bar", SiteRightBar);
        customElements.define("site-footer", SiteFooter);
        customElements.define("site-foot", SiteFoot);
        customElements.define("site-nav", SiteNavigation);

        this.head = document.head;
    }

    add_style_sheet(href) {
        let style_sheet = document.createElement("link");
        style_sheet.setAttribute("href", href);
        style_sheet.setAttribute("rel", "stylesheet");
        this.head.appendChild(style_sheet);
        return style_sheet;
    }
    
    add_script(src) {
        let script = document.createElement("script");
        script.setAttribute("src", src);
        this.head.appendChild(script);
        return script;
    }
    
    add_base(href) {
        let base = document.createElement("base");
        base.setAttribute("href", href);
        this.head.appendChild(base);
        return base;
    }
    
    add_title(text) {
        let title = document.createElement("title");
        title.textContent = text;
        this.head.appendChild(title);
        this.title = text;
        return title;
    }

    add_navigation(title, menu) {
        let nav = document.querySelector("site-nav");
        let details = document.createElement("details");
        let attr = document.createAttribute("open");
        details.setAttributeNode(attr);
        let summary = document.createElement("summary");
        summary.innerText = title;
        details.appendChild(summary);
        nav.appendChild(details);
        let section = document.createElement("section");
        details.appendChild(section);
        let global = menu;
        for (let i of global) {
            let a = document.createElement("a");
            a.setAttribute("href", i.href);
            a.innerText = i.innerText;
            section.appendChild(a);
        }
    }
}
