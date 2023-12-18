clean:
	@rm -rf *.log *.dat *.lprof *.egg-info build dist
publish:
	@python setup.py sdist
	@twine upload dist/*
