#!/usr/bin/python3

from os import scandir as ls

def __passing(*a, **b):
    """Do nothing"""
    pass

def partial(function, *a, **b):
    """Get function with substituted arguments"""
    def func(*c, **d):
        return function(*a, *c, **b, **d)
    return func

def filepath(filename: str, dirs: list):
    """Get full path to file [filename] in place dirs[0]/dirs[1]/dirs[2]/..."""
    return "/".join(dirs) + "/" + filename

def extension(filename: str):
    """Get extension of file with name [filename]"""
    if "." not in filename:
        return None
    tmp = filename.split(".")
    if tmp[-1][0] == '/':
        return None
    return tmp[-1]

def handle(handler: callable = __passing, root: list = ["."], extensions: list = None):
    """Handle by [handler] all files in directory [root] with extension .[extension]"""
    with ls("/".join(root)) as it:
        for entry in it:
            if entry.is_file():
                if extensions:
                    if extension(entry.name) not in extensions:
                        continue
                handler(filepath(entry.name, root))
            else:
                if "." in entry.name:
                    continue
                tmp = root.copy()
                tmp.append(entry.name)
                handle(handler, tmp, extensions)

def printer(filepath: str):
    """Print path to file and filename in template /[path]/filename"""
    print(filepath[1:])

class File:
    """Class of file"""
    def __init__(self, filename):
        self.filename = filename
        self.text = None
    
    def open(self):
        if self.text:
            raise Exception(f"\n--- File {self.filename} is already opened ---\n")
        else:
            try:
                with open(self.filename, mode = 'r') as file:
                    self.text = file.read()
            except Exception as exception:
                print(f"\n--- While opening file {self.filename} I've got an error: {exception} ---\n")
    
    def close(self, save: bool = True):
        if not self.text:
            raise Exception(f"\n--- There is no file to close or file {self.filename} is already closed ---\n")
        else:
            if save:
                self.save()
            self.text = None
    
    def save(self):
        if not self.text:
            raise Exception(f"\n--- There is nothing to save in {self.filename} ---\n")
        else:
            with open(self.filename, mode = 'w') as file:
                file.write(self.text)
    
    def replace(self, old: str, new: str = ""):
        if not self.text:
            raise Exception(f"\n--- There is no file to replace ---\n")
        else:
            self.text = self.text.replace(old, new)

def replacer(filename, old, new):
    file = File(filename)
    file.open()
    file.replace(old, new)
    file.close()
    
OPENING = "opening"
CLOSING = "closing"
CLOSED = "closed"
    
def tag(tag, properties, tag_type: str = OPENING):
    assert tag_type in (OPENING, CLOSING, CLOSED)
    result = '/' if tag_type == CLOSING else ''
    result += tag
    for name, value in properties:
        result += f" {name}={value}"
    result += ' /' if tag_type == CLOSED else ''
    return f"<{result}>"
