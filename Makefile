PYTHON := .venv/bin/python

install: | $(PYTHON)
	poetry install

generate: $(PYTHON)
	poetry run generate

$(PYTHON):
	poetry install

clean:
	rm -rf ansible/guhcampos/docker/roles/*
	rm -rf ansible/guhcampos/podman/roles/*

.DEFAULT_GOAL := generate
