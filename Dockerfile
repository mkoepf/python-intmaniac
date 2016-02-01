FROM python:3-onbuild

MAINTAINER Axel Bock <mr.axel.bock@gmail.com>

ENTRYPOINT [ "intmaniac", "-c", "/intmaniac/intmaniac.yaml"]
