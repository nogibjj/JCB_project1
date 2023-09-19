install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

# test
test:
	python -m pytest -vv --cov=main src/test_*.py

# format
format:	
	black src/*.py
	nbqa black src/*.ipynb

# lint
lint:
	# pylint --disable=R,C --disable=unnecessary-pass --ignore-patterns=test_.*?py src/*.py
	nbqa ruff src/*.ipynb
	ruff check src/*.py


# deploy

all: install lint format test 
