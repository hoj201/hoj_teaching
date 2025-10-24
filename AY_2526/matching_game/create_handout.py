import io
from proportional_relationships import Linear, Rational
from latex_writer import LatexWriter
from typing import List, LiteralString, Tuple

preamble = r"""\documentclass{article}
\usepackage{amsmath}
\usepackage{multicol}
\usepackage[paperwidth=5.5in, paperheight=8.5in, margin=0.2in]{geometry}
\usepackage{pgfplots}
\usepackage{xcolor}
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

fruits = [
    "apple", "pomegranite", "orange", "strawberry", "grape", "guava", "banana", "melon", "plum"
]

animals = [
    "cow", "chicken", "goose", "goat", "bunny", "tiger", "lion", "bat"
]



class Group(object):
    def __init__(self, f: Linear, words: List[str]):
        assert(len(words)==4)
        self.words = words
        self.f = f
    
    def tex(self) -> str:
        words = self.words
        def divider(word, lw: LatexWriter):
            lw.write("\n" + "\\vspace{2ex}")
            lw.write("\\" + "textcolor" + "{red}{" + word + "}")
            lw.write(divider_text)

        with io.StringIO() as buffer:
            writer = LatexWriter(buffer)
            writer.write(self.f.to_latex())
            divider(words[0], writer)
            writer.write(self.f.pgfplot())
            divider(words[1], writer)
            writer.write(self.f.table_tex())
            divider(words[2], writer)
            writer.write(self.f.description)
            divider(words[3], writer)
            buffer.seek(0)
            return buffer.read()
        
        

def create_match_game_latex(buffer):
    x = Linear(slope=1, intercept=0)
    one = Linear(slope=0, intercept=1)
    functions = [
        Linear(
            slope=3, intercept=0,
            description=u"Botan rice candy costs $3.00 per box"
        ),
        Linear(
            slope=0.5, intercept=0,
            description="A car travels one mile in two minutes"
        ),
        Linear(
            slope=Rational(2,3), intercept=0,
            description="For every 3 cups of water we need 2 cups sugar"
        ),
        Linear(
            slope=1, intercept=0,
            description="Every student gets one sticker"
        ),
        Linear(
            slope=Rational(1,3), intercept=0,
            description="I use a full tank of gas every three days"
        )
    ]

    groups = [
        Group(f, words=[w1,w2,w3,w4]) for f, w1, w2, w3, w4 in zip(functions, adjectives, names, fruits, animals)
    ]
    writer = LatexWriter(buffer)
    writer.write(preamble)
    # Write the riddles
    with writer.environment("document"):
        for group in groups:
            writer.write(group.tex())
            writer.write(r"\pagebreak")
        
        # write the answer key
        with writer.environment("center"):
            writer.write(r"\Large Answer Key")
        with writer.environment("itemize"):
            for group in groups:
                writer.write(r"\item " + ":".join(group.words))

if __name__ == "__main__":
    with io.StringIO() as buffer:
        create_match_game_latex(buffer)
        buffer.seek(0)
        print(buffer.read())
    