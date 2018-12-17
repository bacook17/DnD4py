VERSION := $(shell python -c "import DnD4py; print(DnD4py.__version__)")

install:
	pip install . --upgrade

upload: install
	python setup.py sdist bdist_wheel
	twine upload dist/DnD4py-$(VERSION)*
