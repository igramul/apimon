# System Python
PYTHON := python3
BIN := ./venv/bin
VERSION := $(shell git describe --tags --always)

.PHONY: all
all: start

.PHONY: start
start: version.py
	$(BIN)/gunicorn -b :5001 --access-logfile - --error-logfile - flaskapp:app

version.py: .git
	echo version = \"$(VERSION)\" > $@
	echo commit = \"`git rev-parse HEAD`\" >> $@
	echo commit_short = \"`git rev-parse --short HEAD`\" >> $@

venv:
	$(PYTHON) -m venv venv

.PHONY: venv-upgrade
venv-upgrade: venv
	$(BIN)/pip install --upgrade pip setuptools

.Phony: install
install: venv venv-upgrade
	$(BIN)/pip install -r requirements.txt

.PHONY:
clean:
	rm -f version.py

.PHONY: venv-clean
venv-clean:
	rm -rf venv

.PHONY: clean-all
clean-all: clean venv-clean

.PHONY: test
test:
	$(BIN)/$(PYTHON) -m unittest discover tests "*_test.py"
