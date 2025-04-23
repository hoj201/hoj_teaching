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


divider_text = r"""\vspace{2in}
\hrule
\vspace{0.5in}
"""

adjectives = [
    "grimy", "dazzling", "brittle", "sneaky", "lush", "brash", "mellow", "eerie", "quaint", "fierce",
    "foggy", "vibrant", "hollow", "silky", "zesty", "jagged", "nimble", "wistful", "clumsy", "radiant",
    "shabby", "bumpy", "moody", "plush", "rustic", "timid", "quirky", "gaudy", "mellow", "spiky"
]
adjectives.sort()

names = [
    "Liam", "Olivia", "Noah", "Emma", "Oliver", "Ava", "Elijah", "Sophia", "James", "Isabella",
    "William", "Mia", "Benjamin", "Charlotte", "Lucas", "Amelia", "Henry", "Harper", "Alexander", "Evelyn",
    "Daniel", "Abigail", "Matthew", "Ella", "Sebastian", "Scarlett", "Jack", "Luna", "Owen", "Chloe"
]



class Match(object):
    def __init__(self, pf: PiecewiseFunction, word1: str, word2: str):
        self.pf = pf
        self.word1 = word1
        self.word2 = word2

    def tex(self):
        with io.StringIO() as buffer:
            writer = LatexWriter(buffer)
            writer.write(self.pf.tex())
            writer.write(self.word1)
            writer.write(divider_text)
            writer.write(self.pf.pgfplot())
            writer.write(r"\vspace{2ex}")
            writer.write(self.word2)
            buffer.seek(0)
            return buffer.read()

class Handouts(object):
    def __init__(self, matches: List[Match]):
        self.matches = matches

    def tex(self):
        with io.StringIO() as buffer:
            writer = LatexWriter(buffer)
            writer.write(preamble)
            # Write the riddles
            with writer.environment("document"):
                for match in self.matches:
                    writer.write(match.tex())
                    writer.write(r"\pagebreak")
                
                # write the answer key
                with writer.environment("center"):
                    writer.write(r"\Large Answer Key")
                for match in self.matches:
                    with writer.environment("itemize"):
                        writer.write(r"\item " + match.word1 + " : " + match.word2)
            buffer.seek(0)
            return buffer.read()

if __name__ == "__main__":
    x = Polynomial({1:1})
    one = Polynomial({0:1})
    pf_list = [
        PiecewiseFunction([Interval(-4,-1,True, True), Interval(-1,4, False, True)], [2*x-one, 2*x]),
        PiecewiseFunction([Interval(-10,-2,True,False), Interval(-2,0, True,True), Interval(0,10,False,True)], [2*one, -x, -2*one])
    ]
    matches = [Match(pf_list[k], adjectives[k], names[k]) for k in range(len(pf_list))]
    handouts = Handouts(matches)
    print(handouts.tex())