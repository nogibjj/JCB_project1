install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

# test
test:
	python -m pytest -vv --cov=main test_*.py

# format
format:	
	black *.py

# lint
lint:
	pylint --disable=R,C --disable=unnecessary-pass --ignore-patterns=test_.*?py *.py
# container-lint

# deploy

all: install lint format test 