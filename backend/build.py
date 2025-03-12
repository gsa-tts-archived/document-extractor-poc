# uv run build.py

import shutil
import subprocess
import uuid
from pathlib import Path


def execute(program, *args):
    subprocess.call([program, *args])


def uv(*args):
    execute("uv", *args)


def cp(*args):
    execute("cp", *args)


def docker(*args):
    execute("docker", *args)


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
    uv(
        "pip",
        "install",
        "--no-installer-metadata",
        "--no-compile-bytecode",
        "--target",
        build_dir.as_posix(),
        "-r",
        requirements_txt.as_posix(),
    )

    # put our code in the build
    our_code_path = "src"
    our_code = build_dir.joinpath(our_code_path)
    print(f"Copying our code to {our_code.as_posix()}")
    shutil.copytree(src=our_code_path, dst=our_code, dirs_exist_ok=True)

    # build the docker image
    docker_image_id = str(uuid.uuid4())
    print(f"Building docker image {docker_image_id} for tesseract")
    docker("build", ".", "-t", docker_image_id)

    # run the docker container with a volume to mount the bin and lib64 directories
    docker_container_id = str(uuid.uuid4())
    print(f"Create docker container {docker_container_id}")
    docker("create", "--name", docker_container_id, docker_image_id)

    # copy the bin and lib64 directories
    lib_dir = build_dir.joinpath("lib")
    lib_dir.mkdir(parents=True, exist_ok=True)
    # docker("cp", f"{docker_container_id}:/usr/lib64", lib_dir.as_posix())
    docker("cp", "-L", f"{docker_container_id}:/usr/lib64/liblept.so", lib_dir.as_posix())
    docker("cp", "-L", f"{docker_container_id}:/usr/lib64/libtesseract.so", lib_dir.as_posix())
    docker("cp", "-L", f"{docker_container_id}:/usr/lib64/libpng16.so.16", lib_dir.as_posix())
    bin_dir = build_dir.joinpath("bin")
    bin_dir.mkdir(parents=True, exist_ok=True)
    docker("cp", f"{docker_container_id}:/usr/bin/tesseract", bin_dir.as_posix())

    # zip everything
    lambda_zip = dist_folder.joinpath("lambda")
    print(f"Creating distribution zip at {lambda_zip.as_posix()}.zip")
    shutil.make_archive(lambda_zip, "zip", build_dir)


if __name__ == "__main__":
    build()
