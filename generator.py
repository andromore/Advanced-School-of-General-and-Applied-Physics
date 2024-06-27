#!/usr/bin/python3

from lib import *

print("Generator of HTML-pages")
filepath = input("Enter path of file: ")
h1 = Tag("h1", input("Enter h1: "))
h2 = []
while True:
    tmp = input("Enter h2: ")
    if not tmp:
        break
    h2.append(Tag("h2", tmp))

n = filepath.count('/')
if n == 1:
    root = '.'
elif n == 2:
    root = ".."
elif n >= 3:
    root = ".." + "/.." * (n - 2)
else:
    raise

file = File(filepath)
text = parse(File.open("./structure.html").text)
text.children[3].children[1].children.append(Tag("base", href=root))
text.children[3].children[3].children[3].children[3].children.append(h1)
for i in h2:
    text.children[3].children[3].children[3].children[3].children.append(i)

file.write(str(text))
file.close()
