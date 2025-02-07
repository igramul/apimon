# System Python
PYTHON := python3
BIN := ./venv/bin
VERSION := $(shell git describe --tags)
CONTAINER_RUNTIME:=docker
IMAGE_NAME:=apimon

.PHONY: all
all: image

.PHONY: start
start: image stop
	$(CONTAINER_RUNTIME) run -d --restart=always --name $(IMAGE_NAME) -p 8088:5000 -e MC_SERVER_LIST=$(MC_SERVER_LIST) $(IMAGE_NAME):$(VERSION)

.PHONY: stop
stop:
	$(CONTAINER_RUNTIME) stop $(IMAGE_NAME) || true &&  $(CONTAINER_RUNTIME) rm $(IMAGE_NAME) || true

.PHONY: image
image: venv version.py
	$(CONTAINER_RUNTIME) build . -t $(IMAGE_NAME):$(VERSION)

.PHONY: version.py
version.py:
	echo version = \"$(VERSION)\" > $@
	echo commit = \"`git rev-parse HEAD`\" >> $@
	echo commit_short = \"`git rev-parse --short HEAD`\" >> $@

venv:
	$(PYTHON) -m venv venv
	$(BIN)/pip install -r requirements.txt

.PHONY: venv-upgrade
venv-upgrade: venv
	$(BIN)/pip install --upgrade pip setuptools

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
