#!/usr/bin/python3

from lib import *

print("Generator of HTML-pages")
filepath = input("Enter path of file: ")
title = input("Enter h1 of page: ")
n = filepath.count('/')
file = File(filepath)

head = Tag("div", '')
head["id"] = "head"
foot = Tag("div", '')
foot["id"] = "foot"
left = Tag("div", '')
left["id"] = "left-bar"
right = Tag("div", '')
right["id"] = "right-bar"
body = Tag("div", left, Tag("main",
                            Tag("h1", title)), right)
body["id"] = "body"

text = "<!doctype html>" + str(Tag("html",
                                   Tag("head", Tag("base", href='.' * n)),
                                   Tag("body", Tag("header", head), body, Tag("footer", foot))))

file.write(text)
file.close()

