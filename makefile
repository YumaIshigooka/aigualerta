# Detect the operating system
ifeq ($(OS),Windows_NT)
    PYTHON := python
    PIP := pip
    RM := del /f /s /q
	VENV_CREATE := python -m venv
    VENV_ACTIVATE := .venv\Scripts\activate
else
    PYTHON := python3
    PIP := pip3
    RM := rm -rf
    VENV_CREATE := python3 -m venv
    VENV_ACTIVATE := source .venv/bin/activate
endif

source := ./src
interface := ./src/interface
tabs := ./src/interface/tabs
tests := ./tests
testInterface := ./tests/src/interface
testTabs := ./tests/src/interface/tabs

.PHONY: test coverage htmlcov clean install start venv

# --- Virtual Environment ---
venv:
	$(VENV_CREATE) .venv  # Create the virtual environment

# --- Installation ---
install: venv  # Create virtual environment before installing
	$(VENV_ACTIVATE) && $(PIP) install -e .

# --- Running the application ---
start:
	$(VENV_ACTIVATE) && $(PYTHON) -m streamlit run src/aigualerta/main.py

# --- Testing ---
test:
	$(VENV_ACTIVATE) && $(PYTHON) -m pytest --cov=./ --cov-report term-missing

htmlcov: coverage
	$(VENV_ACTIVATE) && $(PYTHON) -m pytest --cov=./ --cov-report html

# --- Cleaning ---
clean:
	$(RM) .coverage htmlcov
	$(RM) $(source)/__pycache__/
	$(RM) $(interface)/__pycache__/
	$(RM) $(tabs)/__pycache__/
	$(RM) $(tests)/__pycache__/
	$(RM) $(testInterface)/__pycache__/
	$(RM) $(testTabs)/__pycache__/
	$(RM) .pytest_cache
	$(RM) dist build $(source)/*.egg-info