from typing import Optional, TextIO

class LatexWriter:
    def __init__(self, file: TextIO) -> None:
        self.file = file

    def write(self, text: str) -> None:
        self.file.write(text + '\n')

    def environment(self, name: str, options: str = '') -> 'LatexEnvironment':
        return LatexEnvironment(self.file, name, options)


class LatexEnvironment:
    def __init__(self, file: TextIO, name: str, options: str = '') -> None:
        self.file = file
        self.name = name
        self.options = options

    def __enter__(self) -> None:
        if self.options:
            self.file.write(f"\\begin{{{self.name}}}[{self.options}]\n")
        else:
            self.file.write(f"\\begin{{{self.name}}}\n")

    def __exit__(self,
                 exc_type: Optional[type],
                 exc_val: Optional[BaseException],
                 exc_tb: Optional[object]) -> None:
        self.file.write(f"\\end{{{self.name}}}\n")

if __name__ == "__main__":
    import io
    buffer: TextIO = io.StringIO()
    writer = LatexWriter(buffer)

    with writer.environment("tikzpicture"):
        writer.write("picture code goes here")

    buffer.seek(0)
    output = buffer.read()
    print(output)