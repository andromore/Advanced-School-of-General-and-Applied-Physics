#!/usr/bin/python3

"""Source functions"""

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

"""Function handle() for recursive deals with files"""

def handle(handler: callable = __passing, root: list[str] = ["."], extensions: list = None):
    """Handle by [handler] all files in directory [root] with extension .[extension]"""
    from os import scandir as ls
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
                
"""Handlers for handle()"""

def printer(filepath: str):
    """Print path to file and filename in template /[path]/filename"""
    print(filepath[1:])

def replacer(filename, old, new):
    """Replace all [old] to [new]"""
    file = File(filename)
    file.open()
    file.replace(old, new)
    file.close()

""" XML\HTML parsing """

class Comment:
    """XML\HTML Comment"""
    
    def __init__(self, text: str):
        assert type(text) == str, ValueError("\n--- Comment contains <str> ---\n")
        self._text = text
    
    def __str__(self):
        return f"<!-- {self.text} -->"
    
    @property
    def text(self) -> str:
        return self._text
    
    @text.setter
    def text(self, value: str):
        assert type(value) == str, ValueError("\n--- Comment contains <str> ---\n")
        self._text = value

class Tag:
    """XML\HTML tag"""
    
    def __init__(self, tag, *args, **kwargs: str | list[str]):
        """kwargs key "_class" will be turned to "class" """
        assert type(tag) == str, ValueError("\n--- Tag must be <str> ---\n")
        for i in args:
            assert type(i) in (str, Comment, Tag), ValueError("\n--- Children must be XML\HTML tags ---\n")
        for i in kwargs.keys():
            assert " " not in i, KeyError("\n--- Key mustn't contain spaces ---\n")
            assert type(kwargs[i]) in (list, str), ValueError("\n--- Values must be <str> or <list> of <str> ---\n")
            if type(kwargs[i]) == list:
                for i in kwargs[i]:
                    assert type(kwargs[i]) == str, ValueError("\n--- Values must be <str> or <list> of <str> ---\n")
        self._tag = tag
        self._children = list(args)
        self._attributes = kwargs
    
    def __str__(self):
        result = self._tag
        for key in self._attributes.keys():
            result += f" {key}=\"{self._attributes[key] if type(self._attributes[key]) == str else ' '.join(self._attributes[key])}\""
        if self._children:
            children = ""
            for i in self._children:
                children += str(i)
            return f"<{result}>{children}</{self._tag}>"
        return f"<{result} />"
        
    def __getitem__(self, key):
        assert type(key) == str, ValueError("\n--- Type of [key] must be <str> ---\n")
        for i in self._attributes.keys():
            assert " " not in i, KeyError("\n--- Key mustn't contain spaces ---\n")
        if key not in self._attributes.keys():
            return None
        return self._attributes[key]
    
    def __setitem__(self, key, value):
        assert type(key) == str or type(value) in (str, list), ValueError("\n--- Type of [key] and [value] must be <str> or <list[str]> ---\n")
        if type(value) == list:
            for i in value:
                assert type(i) == str, ValueError("\n--- Type of [key] and [value] must be <str> or <list[str]> ---\n")
        for i in self._attributes.keys():
            assert " " not in i, KeyError("\n--- Key mustn't contain spaces ---\n")
        self._attributes[key] = value
        
    def __delitem__(self, key):
        assert type(key) == str, ValueError("\n--- Type of [key] must be <str> ---\n")
        for i in self._attributes.keys():
            assert " " not in i, KeyError("\n--- Key mustn't contain spaces ---\n")
        assert key in self._attributes.keys(), KeyError("\n--- It is very difficult to kill a dead ---\n")
        del self._attributes[key]
    
    @property
    def tag(self) -> str:
        return self._tag
    
    @property
    def children(self) -> list:
        return self._children
    
    @property
    def attributes(self) -> list[str]:
        return self._attributes.keys()
    
    def configure(self, value: str):
        """Configure tag"""
        assert type(value) == str, ValueError("\n--- Tag must be <str> ---\n")
        self._tag = value
