install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

# test
test:
	python -m pytest -vv --cov=main src/test_*.py

# format
format:	
	black src/*.py

# lint
lint:
	pylint --disable=R,C --disable=unnecessary-pass --ignore-patterns=test_.*?py src/*.py
# container-lint

# deploy

all: install lint format test 
