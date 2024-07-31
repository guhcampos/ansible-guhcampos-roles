from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from pathlib import PosixPath, Path
from typing import List


class CollectionSettings(BaseSettings):
    """ """

    model_config = SettingsConfigDict(env_prefix="ANSIBLE_GUHCAMPOS_")

    namespace_path: PosixPath = Field(
        default=Path(__file__).parent / Path("../../ansible/guhcampos")
    )
    cookiecutter_contexts_path: PosixPath = Field(
        default=Path(__file__).parent / Path("../../cookiecutter/contexts")
    )
    cookiecutter_templates_path: PosixPath = Field(
        default=Path(__file__).parent / Path("../../cookiecutter/templates")
    )
    container_runtimes: List[str] = Field(
        default=["docker", "podman"],
    )
