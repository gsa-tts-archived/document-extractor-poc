# uv run build.py

import subprocess
from pathlib import Path
import shutil
import os


def execute(program, *args):
    subprocess.call([program, *args])


def uv(*args):
    execute("uv", *args)


def cp(*args):
    execute("cp", *args)


def build():
    dist_folder = Path("dist")
    build_dir = dist_folder.joinpath("build")
    build_dir.mkdir(parents=True, exist_ok=True)

    uv("export", "--frozen", "--no-dev", "--no-editable", "-o", "requirements.txt")
    uv("pip", "install", "--no-installer-metadata", "--no-compile-bytecode", "--target", build_dir.as_posix(), "-r", "requirements.txt")

    our_code_path = "src"
    shutil.copytree(
        src=our_code_path,
        dst=build_dir.joinpath(our_code_path).as_posix(),
        dirs_exist_ok=True
    )

    shutil.make_archive(dist_folder.joinpath("lambda"), "zip", build_dir)


if __name__ == "__main__":
    build()