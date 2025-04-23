from typing import List, LiteralString, NamedTuple, Union, Dict
from latex_writer import LatexWriter
from io import StringIO
from abc import ABC, abstractmethod
from copy import deepcopy

Numeric = Union[float, int]

class Interval(NamedTuple):
    start: int
    end: int
    left: bool
    right: bool

    def __lt__(self, other):
        return self.start < other.start

    def tex(self):
        tex = f"{self.start}"
        if self.left:
            tex += " \\leq x "
        else:
            tex += " < x "
        if self.right:
            tex += f"\\leq {self.end}"
        else:
            tex += f"< {self.end}"
        return tex
    
    def __contains__(self, x: Numeric):
        if self.left and x==self.begin:
            return True
        if self.right and x==self.end:
            return True
        return x < self.end and x > self.begin
    
class Function(ABC):

    @abstractmethod
    def tex(self) -> LiteralString:
        pass

    @abstractmethod
    def eval(self, x: Numeric) -> Numeric:
        pass


class Polynomial(Function):
    """A polynomial"""
    def __init__(self, coefficients: Dict[int, int]):
        self.coefficients = coefficients
        self.powers = sorted(coefficients.keys(), reverse=True)

    def eval(self, x: Numeric):
        return sum([coef*x**pow for pow, coef in self.coefficients.items()])
    
    def tex(self):
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

        s = " +".join([
            monomial_tex(p, self.coefficients[p]) for p in self.powers
        ])
        return s.replace("+-", "-")
    
    def pgf(self):
        s = "+".join(["{}*x^{}".format(self.coefficients[p],p) for p in self.powers])
        return s.replace("+-", "-")

    def __add__(self, other):
        coefficients = deepcopy(self.coefficients)
        for p in other.powers:
            if p not in self.powers:
                coefficients[p] = other.coefficients[p]
            else:
                coefficients[p] += other.coefficients[p]
            if coefficients[p] == 0:
                coefficients.pop(p)
        return Polynomial(coefficients)

    
    def __iadd__(self, other):
        for p in other.powers:
            if p not in self.powers:
                self.coefficients[p] = other.coefficients[p]
            else:
                self.coefficients[p] += other.coefficients[p]
            if self.coefficients[p] == 0:
                self.coefficients.pop(p)
        self.powers = sorted(self.coefficients.keys(), reverse=True)
    
    def __neg__(self):
        return Polynomial({k:-v for k,v in self.coefficients.items()})

    def __sub__(self, other):
        return self.__add__(other.__neg__())
    
    def __isub__(self, other):
        self.__iadd__(other.__neg__())

    def __mul__(self, other):
        if isinstance(other, int):
            return Polynomial({k:other*v for k,v in self.coefficients.items()})
        raise NotImplementedError()
    
    def __lmul__(self, other):
        return self.__mul__(other)
    
    def __rmul__(self, other):
        return self.__mul__(other)


class PiecewiseFunction(Function):
    def __init__(self, domains: List[Interval], functions: List[Function]):
        self.functions = functions
        self.domains = domains
        xmin = min([d.start for d in domains])
        xmax = max([d.end for d in domains])
        self.axis_options = r"""axis lines = middle,
            xlabel = $x$, ylabel = $f(x)$,
            domain=-4:4,
            samples=200,
            ymin=-4.5, ymax=4.5,
            xmin=-4.5, xmax=4.5,
            grid=both,
            xtick={-4,-3,-2,-1,1,2,3,4},
            ytick={-4,-3,-2,-1,1,2,3,4},
            enlargelimits=true"""

    def eval(self, x):
        for d, f in zip(self.domains, self.functions):
            if x in d:
                return f.eval(x)
        raise RuntimeError("Domain error")

    def tex(self):
        with StringIO() as buffer:
            writer = LatexWriter(buffer)
            with writer.environment("align*"):
                writer.write("f(x)=")
                with writer.environment("cases"):
                    writer.write(
                        " \\\\ \n".join(
                            [f.tex() + r" & \text{ if } " + d.tex() for f,d in zip(self.functions, self.domains)]
                        )
                    )
            buffer.seek(0)
            tex = buffer.read()
        return tex
    
    def pgfplot(self):
        with StringIO() as buffer:
            writer = LatexWriter(buffer)
            with writer.environment("tikzpicture"):
                with writer.environment("axis", options=self.axis_options):
                        for f,d in zip(self.functions, self.domains):
                            s = "\\addplot[domain={:0}:{:1}]".format(d.start, d.end)
                            s += "{" + f.pgf() + "};"
                            writer.write(s)
                        writer.write("% Open circles at discontinuities")
                        for f,d in zip(self.functions, self.domains):
                            if d.left:
                                s = "\\addplot[only marks, mark=*, fill=black] coordinates"
                            else:
                                s = "\\addplot[only marks, mark=*, fill=white] coordinates"
                            s += "{(" + str(d.start) + "," + str(f.eval(d.start)) + ")};"
                            writer.write(s)
                            if d.right:
                                s = "\\addplot[only marks, mark=*, fill=black] coordinates"
                            else:
                                s = "\\addplot[only marks, mark=*, fill=white] coordinates"
                            s += "{(" + str(d.end) + "," + str(f.eval(d.end)) + ")};"
                            writer.write(s)
            buffer.seek(0)
            tex = buffer.read()
        return tex


if __name__ == "__main__":
    p1 = Polynomial({1:1})
    p2 = Polynomial({1:-1, 2:2}) - p1

    pwf = PiecewiseFunction(domains=[Interval(-1,1,True,True), Interval(1,2,False,True)], functions=[p1,p2])
    print(pwf.pgfplot())

    print(pwf.tex())
