#!/usr/bin/env python

import itertools
from pprint import pprint
from pathlib import Path
from typing import Any, Dict

import yaml
from cookiecutter.main import cookiecutter
from loguru import logger
from pydantic import ValidationError

from .config import CollectionSettings
from .models import RoleGenerationConfig


def main():
    settings = CollectionSettings()
    contexts = _load_contexts(path=settings.cookiecutter_contexts_path)

    for context in contexts:
        _create_docker_role(settings=settings, context=context)
        _create_podman_role(settings=settings, context=context)


def _load_contexts(path: Path):
    """
    scan the whole context directory and return all yaml documents as a list we
    can iteratve over
    """

    def _generate_contexts():
        for filename in path.glob("*.yaml"):
            logger.info(f"loading context from {filename.resolve()}")
            with open(filename, "r") as f:
                for document in itertools.chain(yaml.safe_load_all(f.read())):
                    try:
                        yield RoleGenerationConfig(**document)
                    except ValidationError:
                        pprint(document)
                        raise

    return list(_generate_contexts())


def _create_docker_role(settings: CollectionSettings, context):
    return _create_role(settings=settings, context=context, runtime="docker")


def _create_podman_role(settings: CollectionSettings, context):
    return _create_role(settings=settings, context=context, runtime="podman")


def _create_role(settings: CollectionSettings, context, runtime):
    extra_context = _define_cookiecutter_context(context=context, runtime=runtime)
    service = context.name
    template = _define_cookiecutter_template(
        settings=settings,
        context=context,
    )
    output_dir = _define_cookiecutter_output_dir(
        settings=settings,
        service=service,
        runtime=runtime,
    )
    logger.info(f"generating {runtime}/{service} in {output_dir}")

    cookiecutter(
        template=template,
        no_input=True,
        output_dir=output_dir,
        overwrite_if_exists=True,
        extra_context=extra_context,
    )


def _define_cookiecutter_template(settings: CollectionSettings, context):
    try:
        _template_name = context.template

    except KeyError:
        pprint(context.model_dump())
        raise

    return str((settings.cookiecutter_templates_path / _template_name).resolve())


def _define_cookiecutter_output_dir(settings: CollectionSettings, service, runtime):
    return str((settings.namespace_path / Path(f"{runtime}/roles/")).resolve())


def _define_cookiecutter_context(context, runtime):
    _context = context.model_dump()
    try:
        _cookiecutter_context = _context["context"]
        _service_name = _context["name"]
    except KeyError:
        pprint(context.model_dump())
        raise

    return {
        **_cookiecutter_context,
        "container_runtime": runtime,
        "service_name": _service_name,
    }


if __name__ == "__main__":
    main()
