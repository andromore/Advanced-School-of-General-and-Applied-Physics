def mss(data_x: list, data_y: list):
    """method of smallest squares"""
    assert len(data_x) == len(data_y)
    n = len(data_x)
    x2 = sum(i ** 2 for i in data_x)
    x = sum(i for i in data_x)
    y = sum(i for i in data_y)
    xy = sum(data_x[i] * data_y[i] for i in range(n))
    det = x2 * n - x ** 2
    k = (xy * n - x * y) / det
    b = (x2 * y - xy * x) / det
    return k, b

def table(data):
    """return latex table"""
    result = r"\begin{tabular}{|" + r"c|" * len(data[0]) + "}\n\\hline\n"
    for i in range(len(data)):
        for j in range(len(data[0])):
            result += str(round(data[i][j], 2)) + (r" & " if j != len(data[0]) - 1 else " \\\\\n\\hline\n")
    result += r"\end{tabular}" + "\n"
    return result

class Graph:
    def __init__(self, caption: str = ""):
        self.plots = []
        self.caption = caption
    
    def add_plot(self, data):
        result = ""
        for i in range(len(data[0]) - 1):
            result += r"\addplot coordinates{"
            for j in range(len(data)):
                result += f"({data[j][0]}, {data[j][i + 1]})"
            result += r"};" + "\n"
        self.plots.append(result)
    
    def __str__(self):
        result = r"\begin{figure}[h]" + "\n"
        result += r"\centering" + "\n"
        result +=  r"\begin{tikzpicture}" + "\n"
        result += r"\begin{axis}" + "\n"
        for i in self.plots:
            result += i
        result += r"\end{axis}" + "\n"
        result += r"\end{tikzpicture}" + "\n"
        result += r"\caption" + f"{{{self.caption}}}" + "\n"
        result += r"\label" + f"{{{self.caption}}}" + "\n"
        result += r"\end{figure}" + "\n"
        return result

def graph(data, caption: str = ""):
    """return latex graph"""
    result = r"\begin{figure}[h]" + "\n"
    result += r"\centering" + "\n"
    result +=  r"\begin{tikzpicture}" + "\n"
    result += r"\begin{axis}" + "\n"
    for i in range(len(data[0]) - 1):
        result += r"\addplot coordinates{"
        for j in range(len(data)):
            result += f"({data[j][0]}, {data[j][i + 1]})"
        result += r"};" + "\n"
    result += r"\end{axis}" + "\n"
    result += r"\end{tikzpicture}" + "\n"
    result += r"\caption" + f"{{{caption}}}" + "\n"
    result += r"\label" + f"{{{caption}}}" + "\n"
    result += r"\end{figure}" + "\n"
    return result

def document(text, doc_cls: str = "article"):
    """return latex document"""
    result = r"\documentclass" + f"{{{doc_cls}}}" + "\n"
    result += r"\usepackage{pgfplots}"
    result += r"\begin{document}" + "\n"
    result += text
    result += r"\end{document}" + "\n"
    return result

def create(document, name: str = "file.tex"):
    """create latex document and pdf file"""
    from os import system
    with open(name,mode='w') as file:
        file.write(document)
    system(r"pdflatex " + name)

