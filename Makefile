all: test install

test:
	tox

install:
	pip install --user --upgrade .

clean:
	-rm *.xml
	-rm -rf .tox
	-rm -rf *.egg-info
	-find . -type f -iname "*.pyc" | xargs -r rm
	-find . -type d -iname "__pycache__" | xargs -r rm -rf

deploy: clean
	python setup.py sdist bdist_wheel
	twine upload dist/*

deploy-test: clean
	python setup.py sdist bdist_wheel
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*

help:
	@echo 'Usage:'
	@echo '  make [TARGET]'
	@echo
	@echo 'Targets:'
	@echo '  test'
	@echo '  install'
	@echo '  clean'
	@echo '  help'

.PHONY: all clean install test help
