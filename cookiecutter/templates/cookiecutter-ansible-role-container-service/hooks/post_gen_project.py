import shutil
import os
from pathlib import Path


def main():
    cleanup_extra_files()


def cleanup_extra_files():
    role = "{{cookiecutter.role_name}}"

    if role != "nginx":
        (Path(".") / Path("tasks/_nginx_default_site.yaml")).unlink()
        (Path(".") / Path("tasks/_nginx_ssl.yaml")).unlink()
        (Path(".") / Path("templates/cloudflare.ini.j2")).unlink()
        (Path(".") / Path("templates/default.conf.j2")).unlink()


if __name__ == "__main__":
    main()
