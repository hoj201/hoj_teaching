handout.tex:
	python3 create_handout.py > handout.tex

handout.pdf: handout.tex
	latexmk --pdf handout.tex

clean:
	latexmk -CA