def latex_wrapper(packages: list=None, argpackages: dict=None, cardfrontstyle: tuple=None, cardbackstyle: tuple=None, cardfrontfoot=None, frame=True, cfgfile="avery"):
    text = r"\documentclass[" + cfgfile
    if frame:
        text += ",frame"
    text += r"]{flashcards}" + "\n\n"

    if argpackages:
        for p in argpackages:
            text += r"\usepackage[" + ",".join(opt for opt in argpackages[p]) + "]{" + p + "}\n"
    if packages:
        text += r"\usepackage{" + ",".join(p for p in packages) + "}\n\n"

    if cardfrontstyle:
        text += r"\cardfrontstyle"
        if cardfrontstyle[1]:
            text += "[" + cardbackstyle[1] + "]"
        text += "{" + cardfrontstyle[0] + "}\n"
    if cardbackstyle:
        text += r"\cardbackstyle"
        if cardbackstyle[1]:
            text += "[" + cardbackstyle[1] + "]"
        text += "{" + cardbackstyle[0] + "}\n"

    text += r"\begin{document}" + "\n\n"
    if cardfrontfoot:
        text += r"\cardfrontstyle{" + cardfrontfoot + "}\n\n"
    return text

class Texobject:
    def __init__(self, name, start_keyword, end_keyword, style=""):
        self.name = name
        self.keyword = start_keyword, end_keyword
        self.style = style

    def inside(self, text, last_digit=True, end=False):
        """compares the string to keyword, returns 2 if same, 1 if included, 0 if different.
        end {0,1} start or end keyword"""
        l = len(text)
        if l > len(self.keyword[end]):
            return 0
        if last_digit:
            if text[-1] == self.keyword[end][l-1]:
                if l == len(self.keyword[end]):
                    return 2
                return 1
            return 0
        if text == self.keyword[end]:
            return 2
        if text == self.keyword[end][:l]:
            return 1
        return 0

class Content:
    def __init__(self, texo:Texobject, text:str, title:str="", index:int=None)->None:
        self.texobject = texo
        self.text = text
        self.title = title
        self.index = index

    def html(self):
        pass

    def json(self):
        return {"type" : self.texobject.name, "index" : self.index, "title" : self.title, "content" : self.text}

    def latex(self):
        return f"{self.texobject.keyword[0]}\n{self.text}\n{self.texobject.keyword[1]}"
