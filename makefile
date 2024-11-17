.PHONY: test coverage htmlcov clean

start:
	streamlit run src/interface/main.py 

test:
	pytest
	pytest --cov=./ --cov-report term-missing

clean:
	rm -rf .coverage htmlcov
	rm -rf **/__pycache__/