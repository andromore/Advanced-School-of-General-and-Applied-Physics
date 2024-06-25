#!/usr/bin/python3

from lib import *

print("Generator of HTML-pages")
filepath = input("Enter path of file: ")
h1 = input("Enter h1: ")
h2 = []
while True:
    tmp = input("Enter h2: ")
    if not tmp:
        break
    h2.append(Tag("h2", tmp))

n = filepath.count('/')
file = File(filepath)

text = Document(Declaration("!doctype", "html")), 
Tag("html",
    Tag("head",
        Tag("base", href='.' * n)),
    Tag("body",
        Tag("header",
            Tag("div", '', attributes={"id": "head"})),
        Tag("div", children=[
            Tag("div", '', attributes={
                "id": "left-bar"}),
            Tag("main", children=[
                Tag("h1", h1), *h2]),
            Tag("div", '', attributes={"id": "right-bar"})], attributes={"id": "body"}),
        Tag("footer",
            Tag("div", '', attributes={"id": "foot"}))))

file.write(text)
file.close()
