%/.created:
	mkdir -p $(dir $@)
	touch $@

build/analysis.pdf: build/.created analysis/analysis.tex
	pdflatex -output-directory=build analysis/analysis.tex
