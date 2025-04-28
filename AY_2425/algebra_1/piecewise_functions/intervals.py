import re
from typing import Union

Numeric = Union[int, float]

class Interval:
    def __init__(self, start, end, inclusive_start, inclusive_end):
        self.start = start
        self.end = end
        self.inclusive_start = inclusive_start
        self.inclusive_end = inclusive_end

    @classmethod
    def from_string(cls, s):
        pattern = r"^([\(\[])\s*(-?inf|\-?\d+)\s*,\s*(-?inf|\-?\d+)\s*([\)\]])$"
        match = re.match(pattern, s)
        if not match:
            raise ValueError("Invalid interval format.")

        left_bracket, start, end, right_bracket = match.groups()
        inclusive_start = left_bracket == '['
        inclusive_end = right_bracket == ']'

        # Convert to floats or numbers
        def parse(val):
            return float(val) if 'inf' in val else int(val)

        return cls(parse(start), parse(end), inclusive_start, inclusive_end)

    def __repr__(self):
        left = '[' if self.inclusive_start else '('
        right = ']' if self.inclusive_end else ')'
        return f"{left}{self.start},{self.end}{right}"

    def to_latex(self, variable='x'):
        parts = []
        if self.start == float('-inf'):
            # Only upper bound
            comp = r'\leq' if self.inclusive_end else '<'
            parts.append(f"{variable} {comp} {self.end}")
        elif self.end == float('inf'):
            # Only lower bound
            comp = r'\geq' if self.inclusive_start else '>'
            parts.append(f"{variable} {comp} {self.start}")
        else:
            # Bounded on both sides
            left_op = r'\leq' if self.inclusive_start else '<'
            right_op = r'\leq' if self.inclusive_end else '<'
            parts.append(f"{self.start} {left_op} {variable} {right_op} {self.end}")
        return ' '.join(parts)
    
    def __contains__(self, x: Numeric):
        if self.inclusive_start and x==self.start:
            return True
        if self.inclusive_end and x==self.end:
            return True
        return x < self.end and x > self.start
    
    def __lt__(self, other):
        return self.start < other.start
    
    def __gt__(self, other):
        return self.start > other.start


if __name__ == "__main__":
    I1 = Interval.from_string("(-inf, 1)")
    print(I1.to_latex())
    I2 = Interval.from_string("(-2,9]")
    print(I2.to_latex())
    I3 = Interval.from_string("(-2,inf)")
    print(I3.to_latex())