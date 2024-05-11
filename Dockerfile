FROM ubuntu:latest
LABEL authors="gecko"

ENTRYPOINT ["top", "-b"]