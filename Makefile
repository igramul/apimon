# System Python
PYTHON := python3
BIN := ./venv/bin
PYTEST := $(BIN)/pytest

.PHONY: all
all: test start

.PHONY: start
start:
	$(BIN)/gunicorn -b :5000 --access-logfile - --error-logfile - apimon:app

venv:
	$(PYTHON) -m venv venv

.PHONY: venv-upgrade
venv-upgrade: venv
	$(BIN)/pip install --upgrade pip setuptools

.Phony: install
install: venv venv-upgrade
	$(BIN)/pip install -r requirements.txt

.PHONY: venv-clean
venv-clean:
	rm -rf venv

.PHONY: test
test: install $(PYTEST)
	PYTHONPATH=. $(PYTEST) ./test/

$(PYTEST):
	$(BIN)/pip install pytest