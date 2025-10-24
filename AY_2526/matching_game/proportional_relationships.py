import re
from typing import List, LiteralString, Union, Dict, Self
from latex_writer import LatexWriter
from io import StringIO
from abc import ABC, abstractmethod
from copy import deepcopy

XMIN = 0
X_MAX = 5

def gcd(a: int, b: int) -> int:
    """Compute the greatest common divisor (GCD) of two integers using the Euclidean algorithm."""
    while b != 0:
        a, b = b, a % b
    return abs(a)


class Rational():
    def __init__(self, numerator:int, denominator:int):
        factor = gcd(numerator, denominator)
        self.numerator = numerator // factor
        self.denominator = denominator // factor

    def __mul__(self, other: Self):
        if isinstance(other, int):
            return self.__mul__(Rational(other, 1))
        return Rational(self.numerator*other.numerator, self.denominator*other.denominator)
    
    def __add__(self, other: Self):
        if isinstance(other, int):
            return self.__add__(Rational(other,1))
        return Rational(self.numerator*other.denominator + self.denominator*other.numerator, self.denominator*other.denominator)

    def __repr__(self):
        if self.denominator == 1:
            return str(self.numerator)
        return "\\frac{" + str(self.numerator) + "}{" + str(self.denominator) + "}"
    
    def __str__(self):
        return self.__repr__()
    
    def toFloat(self):
        return self.numerator / self.denominator

Numeric = Union[float, int, Rational]

class Function(ABC):

    @abstractmethod
    def to_latex(self) -> LiteralString:
        pass

    @abstractmethod
    def eval(self, x: Numeric) -> Numeric:
        pass

class Linear(Function):
    """A linear function like y=mx+b"""
    def __init__(self, slope :Numeric, intercept :Numeric, description=None):
        self.slope = slope
        self.intercept = intercept
        self.axis_options = r"""axis lines = middle,
            xlabel = $x$, ylabel = $y$,
            domain=-4:4,
            samples=20,
            ymin=0, ymax=5,
            xmin=0, xmax=5,
            grid=both,
            xtick={-4,-3,-2,-1,1,2,3,4},
            ytick={-4,-3,-2,-1,1,2,3,4},
            enlargelimits=true"""
        self.description = description

    def eval(self, x: Numeric):
        return self.slope * x + self.intercept
    
    def to_latex(self):
        def monomial_tex(power, coef):
            if power==0:
                return str(coef)
            if power==1:
                suffix = "x"
            else:
                suffix = f"x^{power}"
            if coef == 1:
                prefix = ""
            elif coef == -1:
                prefix = "-"
            else:
                prefix = str(coef)
            return prefix + suffix
        
        s = "$y="
        if self.slope == 1:
            s += "x"
        elif self.slope == 0:
            return str(self.intercept)
        else:
            s += str(self.slope) + "x"
        if self.intercept == 0:
            return s + "$"
        s += "+" + str(self.intercept)
        return s.replace("+-", "-") + "$"
    
    def pgf(self):
        s = "+".join(["{}*x^{}".format(self.coefficients[p],p) for p in self.powers])
        return s.replace("+-", "-")

    def pgfplot(self, x_left:int=0, x_right:int=5):
        slope = self.slope
        intercept = self.intercept
        if isinstance(self.slope, Rational):
            slope = self.slope.toFloat()
        if isinstance(self.intercept, Rational):
            intercept = self.intercept.toFloat()
        with StringIO() as buffer:
            writer = LatexWriter(buffer)
            with writer.environment("tikzpicture"):
                with writer.environment("axis", options=self.axis_options):
                    s = "\\addplot[domain={:0}:{:1}]".format(x_left, x_right)
                    if self.intercept != 0:
                        s += "{" + f"{slope}*x + {intercept}" +  "};"
                    else:
                        s += "{" +  f"{slope}*x" +"};"
                    writer.write(s)
            buffer.seek(0)
            tex = buffer.read()
        return tex
    
    def table_tex(self):
        with StringIO() as buffer:
            writer = LatexWriter(buffer)
            with writer.environment("tabular", required=r"|c|c|"):
                writer.write(r"\hline")
                writer.write("$x$ & $y$" + r" \\")
                for x in range(0,4):
                    y = self.eval(x)
                    writer.write(r"\hline")
                    writer.write(f"${x}$ & ${y}$" + r" \\")
                writer.write(r"\hline")
            buffer.seek(0)
            return buffer.read()

    def __add__(self, other: Union[Self, Numeric]):
        if isinstance(other, int):
            return self.__add__(Linear(slope=0, intercept=other))
        return Linear(slope=self.slope+other.slope, intercept=self.intercept+other.intercept)

    
    def __iadd__(self, other: Self):
        self.slope += other.slope
        self.intercept += other.intercept
    
    def __neg__(self):
        return Linear(slope=-self.slope, intercept=-self.intercept)

    def __sub__(self, other):
        return self.__add__(other.__neg__())
    
    def __isub__(self, other):
        self.__iadd__(other.__neg__())


if __name__ == "__main__":
    linear = Linear(slope=2, intercept=1)
    print(linear.pgfplot(-1,4))

