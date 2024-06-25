#!/usr/bin/python3

"""Source functions"""

def __passing(*a, **b):
    """Do nothing"""
    pass

def message(message: str):
    return f"\n--- {message} ---\n"

def partial(function, *a, **b):
    """Get function with substituted arguments"""
    def func(*c, **d):
        return function(*a, *c, **b, **d)
    return func

def filepath(filename: str, dirs: list):
    """Get full path to file [filename] in place dirs[0]/dirs[1]/dirs[2]/..."""
    assert type(filepath) == str and type(dirs) == list
    return "/".join(dirs) + "/" + filename

class File:
    """Class of file"""
    def __init__(self, filepath: str):
        assert type(filepath) == str, ValueError("\n--- Path of file must be <str> ---\n")
        self._filename = filepath
        self._text = None

    def extension(self):
        """Get file extension"""
        if "." not in self._filename:
            return None
        tmp = self._filename.split(".")
        if tmp[-1][0] == '/':
            return None
        if '.' in tmp[-1]:
            raise Exception("\n--- Bad filepath ---\n")
        return tmp[-1]
    
    @property
    def text(self) -> str:
        return self._text
    
    @text.setter
    def text(self, text: str) -> None:
        assert type(text) == str, ValueError("\n--- Text should be <str> ---\n")
        self._text = text
        
    @property
    def name(self) -> str:
        return self._filename
    
    @name.setter
    def name(self, name: str):
        assert type(name) == str, ValueError(message("Name should be <str>"))
        if self._text:
            raise Exception(message("File isn't closed"))
        self._filename = name
        
    @classmethod
    def open(cls, filename: str):
        assert type(filename) == str, ValueError(message("Filename should be <str>"))
        try:
            with open(filename, mode = 'r') as file:
                text = file.read()
            result = cls(filename)
            result.text = text
            return result
        except Exception as exception:
            raise Exception(f"\n--- While opening file {filename} I've got an error: {exception} ---\n")
    
    def close(self, save: bool = True):
        if not self._text:
            raise Exception(f"\n--- There is no file to close or file {self._filename} is already closed ---\n")
        else:
            if save:
                self.save()
            self._text = None
    
    def save(self):
        if not self._text:
            raise Exception(f"\n--- There is nothing to save in {self._filename} ---\n")
        else:
            with open(self._filename, mode = 'w') as file:
                file.write(self._text)
    
    def replace(self, old: str, new: str = ""):
        if not self._text:
            raise Exception(f"\n--- There is no file to replace ---\n")
        else:
            self._text = self._text.replace(old, new)
            
    def write(self, text: str):
        assert type(text) == str
        self._text = text

"""Function handle() for recursive deals with files"""

def handle(handler: callable = __passing, root: list[str] = ["."], extensions: list = None):
    """Handle by [handler] all files in directory [root] with extension .[extension]"""
    from os import scandir as ls
    with ls("/".join(root)) as it:
        for entry in it:
            if entry.is_file():
                if extensions:
                    if File(entry.name).extension() not in extensions:
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
    file = File.open(filename)
    file.replace(old, new)
    file.close()

""" XML\HTML parsing """

class Declaration:
    """XML\HTML Declaration"""
    
    def __init__(self, begin, end, **kwargs: str | list[str]):
        """kwargs key "_class" will be turned to "class" """
        assert type(begin) == str and type(end) == str, ValueError(message("Beginning and ending must be <str>"))
        for i in kwargs.keys():
            assert " " not in i, KeyError("\n--- Key mustn't contain spaces ---\n")
            assert type(kwargs[i]) in (list, str), ValueError("\n--- Values must be <str> or <list> of <str> ---\n")
            if type(kwargs[i]) == list:
                for i in kwargs[i]:
                    assert type(kwargs[i]) == str, ValueError("\n--- Values must be <str> or <list> of <str> ---\n")
        self._attributes = kwargs
        self._begin = begin
        self._end = end
    
    def __str__(self):
        result = self._begin
        for key in self._attributes.keys():
            if not self._attributes[key]:
                result += f" {key}"
                continue
            result += f" {key}=\"{self._attributes[key] if type(self._attributes[key]) == str else ' '.join(self._attributes[key])}\""
        result += f" {self._end}"
        return f"<{result}>"
        
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
            if not self._attributes[key]:
                result += f" {key}"
                continue
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
        
def parse(text: str):
    assert type(text) == str
    alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    
    OPENING = "opening"
    CLOSING = "closing"
    CLOSED = "closed"
    
    def kwargs(text: str):
        tag = ""
        attributes = dict()
        cursor = 0
        eof = len(text)
        while text[cursor] != ' ' and cursor + 1 < eof:
            tag += text[cursor]
            cursor += 1
        if cursor + 1 >= eof:
            return text, attributes
        cursor += 1
        while cursor + 1 < eof:
            key = ""
            value = ""
            while text[cursor] not in '= ' and cursor + 1 < eof:
                key += text[cursor]
                cursor += 1
            if text[cursor] == ' ':
                cursor += 1
                attributes.update({key: ""})
                continue
            cursor += 1
            if text[cursor] == '"':
                cursor += 1
                while text[cursor] != '"' and cursor + 1 < eof:
                    value += text[cursor]
                    cursor += 1
                cursor += 1
                attributes.update({key: value})
                continue
            while text[cursor] != ' ' and cursor + 1 < eof:
                value += text[cursor]
                cursor += 1
            cursor += 1
            attributes.update({key: value})
            continue
        if '' in attributes.keys():
            del attributes['']
        return text, tag, attributes
            
    class ParseTag:
        def __init__(self, text: str):
            text = text.replace('\n', ' ').replace("  ", ' ')
            self.tag = ""
            self.attributes = dict()
            self.type = ""
            if '/' not in text:
                self.type = OPENING
            elif '/' == text[1]:
                self.type = CLOSING
            elif '/' == text[-2]:
                self.type = CLOSED
                self.tag = text[1:-1]
                return
            else:
                raise Exception(message("While parsing was haven't nonetype tag"))
            
        @property
        def closing(self) -> str:
            if self.type in (CLOSED, CLOSING):
                return None
            elif self.type == OPENING:
                return ParseTag(f"</{self.tag}>")
            else:
                raise            
            
        def __str__(self):
            return ""
    
    result = []
    cursor = 0
    results = 0
    eof = len(text)
    
    while cursor + 1 < eof:
        results += 1
        result.append('')
        while text[cursor] != '<' and cursor + 1 < eof:
            result[results - 1] += text[cursor]
            cursor += 1
        results += 1
        cursor += 1
        result.append('<')
        if text[cursor:cursor+3] == "!--":
            cursor += 3
            result[results - 1] += "!--"
            while text[cursor:cursor+3] != "-->" and cursor + 1 < eof:
                result[results - 1] += text[cursor]
                cursor += 1
            cursor += 3
            result[results - 1] += "-->"
            continue
        while text[cursor] != '>' and cursor + 1 < eof:
            if text[cursor] == '\"':
                result[results - 1] += text[cursor]
                cursor += 1
                while text[cursor] != "\"" and cursor + 1 < eof:
                    result[results - 1] += text[cursor]
                    cursor += 1
            result[results - 1] += text[cursor]
            cursor += 1
        cursor += 1
        result[results - 1] += '>'
        
    for i in range(len(result)):
        if len(result[i]) >= 7 and '<!--' == result[i][:4] and '-->' == result[i][-3:]: # Comment
            result[i] = Comment(result[i][4:-3])
        elif len(result[i]) >= 3 and '<' == result[i][0] and '>' == result[i][-1] and result[i][1] not in (alphabet + '/'): # Declaration
            ...
        elif len(result[i]) >= 3 and '<' == result[i][0] and '>' == result[i][-1]: # Tag
            ...
        elif '<' not in result[i] and '>' not in result[i]: # Text
            pass
        else:
            raise Exception(message("While scanning file an error has occurred"))
        
    return result
    
    
file = File.open("./index.html")    
parse(file.text)
