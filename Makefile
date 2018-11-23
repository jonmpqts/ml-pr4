venv/bin/python: requirements.txt
	test -d venv || virtualenv -p python3 venv
	venv/bin/pip install -Ur requirements.txt
	touch venv/bin/python

*.py: venv/bin/python

%/.created:
	mkdir -p $(dir $@)
	touch $@

build/analysis.pdf: build/.created analysis/analysis.tex
	pdflatex -output-directory=build analysis/analysis.tex
	cp analysis/Bibliography.bib build
	cd build && bibtex analysis
	pdflatex -output-directory=build analysis/analysis.tex
	pdflatex -output-directory=build analysis/analysis.tex
