FROM amazonlinux:latest

COPY ./fedora.repo /etc/yum.repos.d/
RUN dnf update -y

RUN dnf install -y tesseract tesseract-devel leptonica-devel pkg-config

RUN chmod -R 755 /usr/bin
RUN chmod -R 755 /usr/lib64
