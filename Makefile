%/.created:
	mkdir -p $(dir $@)
	touch $@

build/analysis.pdf: build/.created analysis/analysis.tex
	pdflatex -output-directory=build analysis/analysis.tex
	cp analysis/Bibliography.bib build
	cd build && bibtex analysis
	pdflatex -output-directory=build analysis/analysis.tex
	pdflatex -output-directory=build analysis/analysis.tex
