import io
from piecewise_functions import PiecewiseFunction, Polynomial, Interval
from latex_writer import LatexWriter
from typing import List, LiteralString, Tuple

preamble = r"""\documentclass{article}
\usepackage{amsmath}
\usepackage{multicol}
\usepackage[paperwidth=5.5in, paperheight=8.5in, margin=0.2in]{geometry}
\usepackage{pgfplots}
\pgfplotsset{compat=1.18}
\usepackage{graphicx} % Required for inserting images
\usepackage{tgadventor}
\renewcommand*\familydefault{\sfdefault} %% Only if the base font of the document is to be sans serif
\usepackage[T1]{fontenc}

\pgfplotsset{
    every axis/.append style={
        scale only axis,
        width=0.75\textwidth,
        xtick={0,0.05,0.1},
    }
}"""


divider_text = "\n" + r"\vspace{2.5in}" + "\n"

adjectives = [
    "grimy", "dazzling", "sneaky", "lush", "brash", "mellow", "eerie", "quaint", "fierce",
    "foggy", "vibrant", "hollow", "silky", "zesty", "jagged", "nimble", "wistful", "clumsy", "radiant",
    "shabby", "bumpy", "moody", "plush", "rustic", "timid", "quirky", "gaudy", "mellow", "spiky"
]
adjectives.sort()

names = [
    "Liam", "Ava", "Soraya", "Ronan", "Hadley", "Jack", "Elijah", "Sophia", "James", "Isabella",
    "William", "Mia", "Benjamin", "Charlotte", "Lucas", "Amelia", "Harper", "Alexander", "Evelyn",
    "Daniel", "Abigail", "Matthew", "Ella", "Sebastian", "Scarlett", "Jack", "Luna", "Owen", "Chloe"
]



class Match(object):
    def __init__(self, pf: PiecewiseFunction, word1: str, word2: str, match_type: str):
        self.pf = pf
        self.word1 = word1
        self.word2 = word2
        self.match_type = match_type

    def to_latex(self):
        if self.match_type == "f2g":
            return self.function2graph_tex()
        if self.match_type == "f2t":
            return self.function2table_tex()
        if self.match_type == "f2d":
            return self.function2description_tex()
        if self.match_type == "g2t":
            return self.graph2table_tex()
        if self.match_type == "g2d":
            return self.graph2description_tex()
        if self.match_type == "t2d":
            return self.table2description()
        raise ValueError(f"unrecognized match_type {self.match_type}")
        

    def _match_tex(self, tex1: str, tex2: str):
        with io.StringIO() as buffer:
            writer = LatexWriter(buffer)
            writer.write(tex1)
            writer.write(self.word1)
            writer.write(divider_text)
            writer.write(tex2)
            writer.write("\n" + r"\vspace{2ex}")
            writer.write(self.word2)
            buffer.seek(0)
            return buffer.read()
        
    def function2graph_tex(self):
        return self._match_tex(self.pf.to_latex(), self.pf.pgfplot())
        
    def function2table_tex(self):
        return self._match_tex(self.pf.to_latex(), self.pf.table_tex())

    def function2description_tex(self):
        return self._match_tex(self.pf.to_latex(), self.pf.description)

    def graph2description_tex(self):
        return self._match_tex(self.pf.pgfplot(), self.pf.description)

    def graph2table_tex(self):
        return self._match_tex(self.pf.pgfplot(), self.pf.table_tex())

    def table2description(self):
        return self._match_tex(self.pf.description, self.pf.table_tex())
        

def create_match_game_latex(buffer):
    x = Polynomial({1:1})
    one = Polynomial({0:1})
    pfs = [
        PiecewiseFunction(
            domains=[Interval.from_string("(-inf,-1)"), Interval.from_string("[-1,1]"), Interval.from_string("(1,inf)")],
            functions=[one, x+2*one, 3*one],
            description="graph holds constant at 1 until x=-1, then rises until it hits 3 at x=1, then stays constant at 3"
        ),
        PiecewiseFunction(
            domains=[Interval.from_string("(-inf,-2)"), Interval.from_string("[-2,1]"), Interval.from_string("(1,inf)")],
            functions=[one, 2*one, 4*one],
            description="graph is constant at a value of 1 until x=-2, where it jumps up by one, and holds constant, then jumps up by two at x=1, and is constant forever after."
        ),
        PiecewiseFunction(
            domains=[Interval.from_string("(-inf,-2)"), Interval.from_string("[-2,1]"), Interval.from_string("(1,inf)")],
            functions=[one, x, one],
        ),
        PiecewiseFunction(
            domains=[Interval.from_string("(-inf,1)"), Interval.from_string("[1,inf)")],
            functions=[x+1, -1*one],
        ),
        PiecewiseFunction(
            domains=[Interval.from_string("(-inf,1)"), Interval.from_string("[1,inf)")],
            functions=[x-1, one],
        ),
        PiecewiseFunction(
            domains=[Interval.from_string("(-inf,-2)"), Interval.from_string("[-2,1]"), Interval.from_string("(1,inf)")],
            functions=[one, -x, one],
        ),
        PiecewiseFunction(
            domains=[Interval.from_string("(-inf,-1)"), Interval.from_string("[-1,1]"), Interval.from_string("(1,inf)")],
            functions=[-one, x, one],
        ),
        PiecewiseFunction(
            domains=[Interval.from_string("(-inf,-2)"), Interval.from_string("[-2,2]"), Interval.from_string("(2,inf)")],
            functions=[-one, x, one],
        )
    ]

    match_types = [
        "g2d",
        "g2d",
        "g2t",
        "g2t",
        "f2g",
        "f2g",
        "f2t",
        "f2t"
    ]

    matches = [
        Match(pf, w1, w2, match_type=mt) for pf, w1, w2, mt in zip(pfs, adjectives, names, match_types)
    ]
    writer = LatexWriter(buffer)
    writer.write(preamble)
    # Write the riddles
    with writer.environment("document"):
        for match in matches:
            writer.write(match.to_latex())
            writer.write(r"\pagebreak")
        
        # write the answer key
        with writer.environment("center"):
            writer.write(r"\Large Answer Key")
        with writer.environment("itemize"):
            for match in matches:
                writer.write(r"\item " + match.word1 + " : " + match.word2)

if __name__ == "__main__":
    with io.StringIO() as buffer:
        create_match_game_latex(buffer)
        buffer.seek(0)
        print(buffer.read())
    