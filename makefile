install:
	pip install . --upgrade

upload:
	python setup.py sdist bdist_wheel
	twine upload dist/*
