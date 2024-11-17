.PHONY: test coverage htmlcov clean

test:
	pytest
	pytest --cov=./ --cov-report term-missing

coverage:
	pytest --cov=./ --cov-report term-missing

htmlcov:
	pytest --cov=./ --cov-report html

clean:
	rm -rf .coverage htmlcov
	find . -name "*.pyc" -delete