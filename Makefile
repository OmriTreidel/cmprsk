
clean_dist:
	rm -rf dist/

.PHONY: test
test:
	pytest --cov=cmprsk --cov-report term-missing cmprsk/tests/ -vv

.PHONY: build
build:
	python setup.py sdist bdist_wheel

.PHONY: deploy
deploy:
	twine upload dist/* --verbose