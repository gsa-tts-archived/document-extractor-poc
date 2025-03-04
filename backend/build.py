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

    if dist_folder.exists():
        print(f"Cleaning {dist_folder.as_posix()} folder")
        shutil.rmtree(dist_folder)

    build_dir = dist_folder.joinpath("build")
    build_dir.mkdir(parents=True, exist_ok=True)

    requirements_txt = dist_folder.joinpath("requirements.txt")

    print(f"Exporting uv dependencies to {requirements_txt.as_posix()}")
    uv("export", "--frozen", "--no-dev", "--no-editable", "-o", requirements_txt.as_posix())

    print(f"Generating dependency distribution in {build_dir.as_posix()}")
    uv("pip", "install", "--no-installer-metadata", "--no-compile-bytecode", "--target", build_dir.as_posix(), "-r", requirements_txt.as_posix())

    our_code_path = "src"
    our_code = build_dir.joinpath(our_code_path)
    print(f"Copying our code to {our_code.as_posix()}")
    shutil.copytree(
        src=our_code_path,
        dst=our_code,
        dirs_exist_ok=True
    )

    lambda_zip = dist_folder.joinpath("lambda")
    print(f"Creating distribution zip at {lambda_zip.as_posix()}.zip")
    shutil.make_archive(lambda_zip, "zip", build_dir)


if __name__ == "__main__":
    build()
