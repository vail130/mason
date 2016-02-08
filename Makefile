test:
	nosetests $$suite

publish:
	python setup.py sdist upload

.PHONY: test
