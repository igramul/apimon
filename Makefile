# System Python
PYTHON := python3
BIN := ./venv/bin
PYTEST := $(BIN)/pytest
INSTALL_DIR=/opt/apimon

.PHONY: all
all: test start

.PHONY: start
start:
	$(BIN)/gunicorn -b :5000 --access-logfile - --error-logfile - apimon:app

.Phony: venv
venv:
	$(PYTHON) -m venv venv
	$(BIN)/pip install --upgrade pip setuptools
	$(BIN)/pip install -r requirements.txt

PHONY: clean-all
clean-all:
	rm -rf venv

.PHONY: test
test: $(PYTEST)
	PYTHONPATH=. $(PYTEST) ./test/

$(PYTEST):
	$(BIN)/pip install pytest

.PHONY: install
install:
	$(PYTHON) -m venv $(INSTALL_DIR)/venv
	$(INSTALL_DIR)/venv/bin/pip install --upgrade pip setuptools
	$(INSTALL_DIR)/venv/bin/pip install -r requirements.txt
	cp -r apimon.py app $(INSTALL_DIR)

