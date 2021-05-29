install:
	pip install -r requirements.txt

#setup:
#	python3 -m venv ~/.finance

#test:
#	python -m pytest -vv --cov=personal-finance tests/*.py

lint:
	pylint --disable=R,C linttest.py

#all: install lint test