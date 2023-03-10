
clean_dist:
	rm -rf dist/


build:
	python setup.py sdist bdist_wheel


deploy:
	twine upload dist/* --verbose