#!/usr/bin/python3

from string import ascii_lowercase, ascii_uppercase

alphabet = ascii_uppercase + ascii_lowercase

"""Source functions"""

def passing(*a, **b):
    """Do nothing"""
    pass

def partial(function, *a, **b):
    """Get function with substituted arguments"""
    def func(*c, **d):
        return function(*a, *c, **b, **d)
    return func

def message(message: str):
    """Generate exception message"""
    return f"\n--- {message} ---\n"

def filepath(filename: str, dirs: list):
    """Get full path to file [filename] in place dirs[0]/dirs[1]/dirs[2]/..."""
    assert type(filename) == str and type(dirs) == list
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

def handle(handler: callable = passing, root: list[str] = ["."], extensions: list = None):
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

""" XML\HTML parsing 
    API: document object model (read/write) """
    
""" Base classes """
    
TAG = "tag"
COMMENT = "comment"
DOCUMENT = "document"
DECLARATION = "declaration"
INSTRUCTION = "instruction"
    
class BaseTag:
    """Based class for XML\HTML tag"""
    
    @property
    def type(self) -> str:
        return self._type
    
    @type.setter
    def type(self, value: str) -> None:
        assert value in (TAG, COMMENT, DOCUMENT, DECLARATION, INSTRUCTION)
        self._type = value
        
class TaggedTag:
    """Based class for XML\HTML tags with tags"""
    
    def _init_tag(self, tag: str):
        """Fast initialization"""
        assert type(tag) == str
        self._tag = tag
    
    @property
    def tag(self) -> str:
        return self._tag
    
    def _str_tag(self) -> str:
        return self._tag
    
class ParentTag:
    """Based class for XML\HTML tags with children"""
    
    def _init_children(self, *args, children: list = None):
        """Fast initialization"""
        for i in args:
            assert type(i) in (str, Declaration, Comment, Tag), ValueError("\n--- Children must be XML\HTML tags ---\n")
        if children:
            assert type(children) == list, ValueError(message("[children] must be <list> of XML\HTML tags"))
            for i in children:
                assert type(i) in (str, Declaration, Comment, Tag), ValueError(message("[children] must be <list> of XML\HTML tags"))
            args = list(args) + children
        self._children = list(args)
        
    def _str_children(self) -> str:
        children = ""
        for i in self._children:
            children += str(i)
        return children
    
    @property
    def children(self) -> list:
        return self._children
    
class AttributesTag:
    """Based class for XML\HTML tags with attributes"""
    
    def _init_attributes(self, attributes: dict[str, str] = None, **kwargs: str | list[str]):
        """Fast initialization"""
        for i in kwargs.keys():
            assert " " not in i, KeyError("\n--- Key mustn't contain spaces ---\n")
            assert type(kwargs[i]) in (list, str), ValueError("\n--- Values must be <str> or <list> of <str> ---\n")
            if type(kwargs[i]) == list:
                for i in kwargs[i]:
                    assert type(kwargs[i]) == str, ValueError("\n--- Values must be <str> or <list> of <str> ---\n")
        if attributes:
            assert type(attributes) == dict, ValueError(message("[attributes] must be dict of <str>: <str>"))
            for i in attributes.keys():
                assert type(i) == str, ValueError(message("[attributes] must be dict of <str>: <str>"))
                assert type(attributes[i]) == str, ValueError(message("[attributes] must be dict of <str>: <str>"))
            kwargs.update(attributes)
        self._attributes = kwargs
        
    def _str_attributes(self) -> str:
        result = ""
        for key in self._attributes.keys():
            if not self._attributes[key]:
                result += f" {key}"
                continue
            result += f" {key}=\"{self._attributes[key] if type(self._attributes[key]) == str else ' '.join(self._attributes[key])}\""
        return result
    
    @property
    def attributes(self) -> list[str]:
        return self._attributes.keys()
    
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
        
""" XML\HTML classes """

class Declaration(AttributesTag, BaseTag):
    """XML\HTML Declaration"""
    
    _type = DECLARATION
    
    def __init__(self, attributes: dict[str: str] = None, **kwargs: str | list[str]):
        """kwargs key "_class" will be turned to "class" """
        self._init_attributes(attributes=attributes, **kwargs)
    
    def __str__(self):
        return f"<?xml{self._str_attributes()}?>"

class Instruction(AttributesTag, TaggedTag, BaseTag):
    """XML\HTML Instruction"""
    
    _type = INSTRUCTION
    
    def __init__(self, tag, attributes: dict[str: str] = None, **kwargs: str | list[str]):
        """kwargs key "_class" will be turned to "class" """
        self._init_attributes(attributes=attributes, **kwargs)
        self._init_tag(tag)
    
    def __str__(self):
        return f"<{self._str_tag()}{self._str_attributes()}>"

class Comment(BaseTag):
    """XML\HTML Comment"""
    
    _type = COMMENT
    
    def __init__(self, text: str):
        assert type(text) == str, ValueError(message("Comment contains <str>"))
        self._text = text
    
    def __str__(self):
        return f"<!-- {self.text} -->"
    
    @property
    def text(self) -> str:
        return self._text
    
    @text.setter
    def text(self, value: str):
        assert type(value) == str, ValueError(message("Comment contains <str>"))
        self._text = value

class Tag(AttributesTag, ParentTag, TaggedTag, BaseTag):
    """XML\HTML tag"""
    
    _type = TAG
    
    def __init__(self, tag, *args, children: list = None, attributes: dict[str: str] = None, **kwargs: str | list[str]):
        self._init_tag(tag)
        self._init_children(*args, children=children)
        self._init_attributes(attributes=attributes, **kwargs)
        
    @property
    def inner(self) -> str:
        return self._str_children()
    
    @property
    def opening(self) -> str:
        if not self._children:
            return f"<{self._str_tag() + self._str_attributes()} />"
        return f"<{self._str_tag() + self._str_attributes()}>"
    
    @property
    def closing(self) -> str | None:
        if self._children:
            return f"</{self._str_tag()}>"
        return None
    
    def __str__(self):
        if self._children:
            return f"{self.opening}{self.inner}{self.closing}"
        return self.opening

class Document(ParentTag, BaseTag):
    """Class of XML\HTML document"""
    
    _type = DOCUMENT
    
    def __init__(self, *args, children: list = None):
        self._init_children(*args, children=children)
        
    def __str__(self) -> str:
        return self._str_children()
        
def parse(text: str):
    """Parse XML\HTML structure from [text]"""
    assert type(text) == str
    
    def kwargs(text: str):
        tag = ""
        attributes = dict()
        cursor = 0
        eof = len(text)
        while cursor < eof and text[cursor] != ' ':
            tag += text[cursor]
            cursor += 1
        if cursor >= eof:
            return tag, attributes
        # text[cursor] == ' ' -> true
        cursor += 1
        while cursor < eof:
            key = ""
            value = ""
            if text[cursor] in " \n\t":
                cursor += 1
                continue
            while cursor < eof and text[cursor] not in " =":
                key += text[cursor]
                cursor += 1
            if cursor >= eof:
                attributes.update({key: value})
                continue
            if text[cursor] == ' ':
                attributes.update({key: value})
                cursor += 1
                continue
            # text[cursor] == '=' -> true
            cursor += 1
            if text[cursor] == '"':
                cursor += 1
                while cursor < eof and text[cursor] != '"':
                    value += text[cursor]
                    cursor += 1
                if cursor >= eof:
                    raise Exception(message("Exception while parsing tag: there are not enough closing quotes"))
                # text[cursor] == '"' -> true
                cursor += 1
                attributes.update({key: value})
                continue
            elif text[cursor] == "'":
                cursor += 1
                while cursor < eof and text[cursor] != "'":
                    value += text[cursor]
                    cursor += 1
                if cursor >= eof:
                    raise Exception(message("Exception while parsing tag: there are not enough closing quotes"))
                # text[cursor] == '"' -> true
                cursor += 1
                attributes.update({key: value})
                continue
            while cursor < eof and text[cursor] != ' ':
                value += text[cursor]
                cursor += 1
            if cursor < eof:
                cursor += 1
            attributes.update({key: value})
        return tag, attributes
    
    result = []
    cursor = 0
    results = 0
    eof = len(text)
    
    while cursor + 1 < eof:
        # Parsing plain text
        results += 1
        result.append('')
        while text[cursor] != '<' and cursor + 1 < eof:
            result[results - 1] += text[cursor]
            cursor += 1
        results += 1
        cursor += 1
        result.append('<')
        if text[cursor:cursor+3] == "!--":
            # Parsing comments
            cursor += 3
            result[results - 1] += "!--"
            while text[cursor:cursor+3] != "-->" and cursor + 1 < eof:
                result[results - 1] += text[cursor]
                cursor += 1
            cursor += 3
            result[results - 1] += "-->"
            continue
        # Tag parsing
        while text[cursor] != '>' and cursor + 1 < eof:
            if text[cursor] == '"':
                result[results - 1] += text[cursor]
                cursor += 1
                while text[cursor] != '"' and cursor + 1 < eof:
                    result[results - 1] += text[cursor]
                    cursor += 1
            elif text[cursor] == "'":
                result[results - 1] += text[cursor]
                cursor += 1
                while text[cursor] != "'" and cursor + 1 < eof:
                    result[results - 1] += text[cursor]
                    cursor += 1
            result[results - 1] += text[cursor]
            cursor += 1
        cursor += 1
        result[results - 1] += '>'
        result[results - 1] = result[results - 1].replace('\n', ' ')
        while "  " in result[results - 1]:
            result[results - 1] = result[results - 1].replace("  ", ' ')

    root = Document()
    now = [root]
    
    for i in range(len(result)):
        if len(result[i]) >= 7 and '<!--' == result[i][:4] and '-->' == result[i][-3:]: # Comment
            now[-1].children.append(Comment(result[i][4:-3]))
        elif len(result[i]) >= 7 and '<?xml' == result[i][:5] and '?>' == result[i][-2:] and result[i][1] not in (alphabet + '/'): # Declaration # There is problems with parsing XML declarations, but HTML doctype declaration is parsed perfectly
            _, attributes = kwargs(result[i][1:-2])
            now[-1].children.append(Declaration(attributes=attributes))
        elif len(result[i]) >= 4 and '<!' == result[i][:2] and '>' == result[i][-1]: # Instruction
            tag, attributes = kwargs(result[i][1:-1])
            now[-1].children.append(Instruction(tag, attributes=attributes))
        elif len(result[i]) >= 3 and '<' == result[i][0] and '>' == result[i][-1]: # Tag
            if result[i][-2] == '/': # Self-closed tag
                tmp = result[i][1:-1]
                tag, attributes = kwargs(tmp)
                now[-1].children.append(Tag(tag, attributes=attributes))
            elif result[i][1] == '/': # Closing tag
                if result[i] != now[-1].closing:
                    raise Exception(message(f'Error while parsing document: "{result[i]}", but expected "{now[-1].closing}"'))
                now[-2].children.append(now[-1])
                if len(now) >= 2:
                    now.pop(-1)
            else: # Opening tag
                tag, attributes = kwargs(result[i][1:-1])
                now.append(Tag(tag, attributes=attributes))
        elif '<' not in result[i] and '>' not in result[i]: # Text
            now[-1].children.append(result[i])
        else:
            raise Exception(message("While scanning file an error has occurred"))
    return root
