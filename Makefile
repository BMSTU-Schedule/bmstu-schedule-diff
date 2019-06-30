init:
	pip3 install pipenv --upgrade
	pipenv install --dev

test:
	pytest

publish:
	pip3 install twine
	python3 setup.py sdist bdist_wheel
	twine upload dist/*
	rm -rf build dist *.egg *.egg-info
