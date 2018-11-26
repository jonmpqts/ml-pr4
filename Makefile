all: build/analysis.pdf

SECONDARY: build/.created \
	build/FrozenLake-v0-vi.json build/FrozenLake-v0-pi.json \
	build/FrozenLake8x8-v0-vi.json build/FrozenLake8x8-v0-pi.json \
	build/FrozenLake-v0-vi-iter-1.png build/FrozenLake-v0-vi-iter-10.png build/FrozenLake-v0-vi-iter-2.png build/FrozenLake-v0-vi-iter-100.png build/FrozenLake-v0-vi-iter-200.png build/FrozenLake-v0-vi-iter-500.png \
	build/FrozenLake-v0-pi-iter-1.png build/FrozenLake-v0-pi-iter-10.png build/FrozenLake-v0-pi-iter-2.png build/FrozenLake-v0-pi-iter-100.png build/FrozenLake-v0-pi-iter-200.png build/FrozenLake-v0-pi-iter-500.png \
	build/FrozenLake8x8-v0-vi-iter-1.png build/FrozenLake8x8-v0-vi-iter-10.png build/FrozenLake8x8-v0-vi-iter-2.png build/FrozenLake8x8-v0-vi-iter-100.png build/FrozenLake8x8-v0-vi-iter-200.png build/FrozenLake8x8-v0-vi-iter-500.png \
	build/FrozenLake8x8-v0-pi-iter-1.png build/FrozenLake8x8-v0-pi-iter-10.png build/FrozenLake8x8-v0-pi-iter-2.png build/FrozenLake8x8-v0-pi-iter-100.png build/FrozenLake8x8-v0-pi-iter-200.png build/FrozenLake8x8-v0-pi-iter-500.png

venv/bin/python: requirements.txt
	test -d venv || virtualenv -p python3 venv
	venv/bin/pip install -Ur requirements.txt
	touch venv/bin/python

*.py: venv/bin/python

%/.created:
	mkdir -p $(dir $@)
	touch $@

build/%-vi.json: build/.created vi.py
	venv/bin/python vi.py $* $@

build/%-pi.json: build/.created pi.py
	venv/bin/python pi.py $* $@

build/%-pi-iter-1.png: build/.created build/%-pi.json policy-map.py
	venv/bin/python policy-map.py build/$*-pi.json 1 $@

build/%-pi-iter-10.png: build/.created build/%-pi.json policy-map.py
	venv/bin/python policy-map.py build/$*-pi.json 10 $@

build/%-pi-iter-20.png: build/.created build/%-pi.json policy-map.py
	venv/bin/python policy-map.py build/$*-pi.json 20 $@

build/%-pi-iter-100.png: build/.created build/%-pi.json policy-map.py
	venv/bin/python policy-map.py build/$*-pi.json 100 $@

build/%-pi-iter-200.png: build/.created build/%-pi.json policy-map.py
	venv/bin/python policy-map.py build/$*-pi.json 200 $@

build/%-pi-iter-500.png: build/.created build/%-pi.json policy-map.py
	venv/bin/python policy-map.py build/$*-pi.json 500 $@

build/%-vi-iter-1.png: build/.created build/%-vi.json policy-map.py
	venv/bin/python policy-map.py build/$*-vi.json 1 $@

build/%-vi-iter-10.png: build/.created build/%-vi.json policy-map.py
	venv/bin/python policy-map.py build/$*-vi.json 10 $@

build/%-vi-iter-20.png: build/.created build/%-vi.json policy-map.py
	venv/bin/python policy-map.py build/$*-vi.json 20 $@

build/%-vi-iter-100.png: build/.created build/%-vi.json policy-map.py
	venv/bin/python policy-map.py build/$*-vi.json 100 $@

build/%-vi-iter-200.png: build/.created build/%-vi.json policy-map.py
	venv/bin/python policy-map.py build/$*-vi.json 200 $@

build/%-vi-iter-500.png: build/.created build/%-vi.json policy-map.py
	venv/bin/python policy-map.py build/$*-vi.json 500 $@

build/analysis.pdf: \
	build/.created \
	analysis/analysis.tex \
	build/FrozenLake-v0-vi-iter-1.png \
	build/FrozenLake-v0-vi-iter-10.png \
	build/FrozenLake-v0-vi-iter-20.png \
	build/FrozenLake-v0-vi-iter-100.png \
	build/FrozenLake-v0-vi-iter-200.png \
	build/FrozenLake-v0-vi-iter-500.png \
	build/FrozenLake-v0-pi-iter-1.png \
	build/FrozenLake-v0-pi-iter-10.png \
	build/FrozenLake-v0-pi-iter-20.png \
	build/FrozenLake-v0-pi-iter-100.png \
	build/FrozenLake-v0-pi-iter-200.png \
	build/FrozenLake-v0-pi-iter-500.png \
	build/FrozenLake8x8-v0-vi-iter-1.png \
	build/FrozenLake8x8-v0-vi-iter-10.png \
	build/FrozenLake8x8-v0-vi-iter-20.png \
	build/FrozenLake8x8-v0-vi-iter-100.png \
	build/FrozenLake8x8-v0-vi-iter-200.png \
	build/FrozenLake8x8-v0-vi-iter-500.png \
	build/FrozenLake8x8-v0-pi-iter-1.png \
	build/FrozenLake8x8-v0-pi-iter-10.png \
	build/FrozenLake8x8-v0-pi-iter-20.png \
	build/FrozenLake8x8-v0-pi-iter-100.png \
	build/FrozenLake8x8-v0-pi-iter-200.png \
	build/FrozenLake8x8-v0-pi-iter-500.png
	pdflatex -output-directory=build analysis/analysis.tex
	cp analysis/Bibliography.bib build
	cd build && bibtex analysis
	pdflatex -output-directory=build analysis/analysis.tex
	pdflatex -output-directory=build analysis/analysis.tex
