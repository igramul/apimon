# System Python
PYTHON := python3
BIN := ./venv/bin
VERSION := $(shell git describe --tags --always)
ifeq ($(shell command -v podman),)
    CONTAINER_RUNTIME := docker
else
    CONTAINER_RUNTIME := podman
endif
IMAGE_NAME:=apimon
include .env

.PHONY: all
all: image

.PHONY: start
start: image stop
	@echo Starting Docker Image \"$(IMAGE_NAME):$(VERSION)\"
	@$(CONTAINER_RUNTIME) run -d --restart=always --name $(IMAGE_NAME) -p 8088:5000 \
	-e ACCESS_TOKEN_URL=$(ACCESS_TOKEN_URL) \
	-e CLIENT_ID=$(CLIENT_ID) \
	-e CLIENT_SECRET=$(CLIENT_SECRET) \
	-e SCOPE=$(SCOPE) \
	$(IMAGE_NAME):$(VERSION)

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
