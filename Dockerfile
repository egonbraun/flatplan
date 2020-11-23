FROM python:3.8.6-buster

LABEL "maintainer" = "Egon Braun <egonbraun@gmail.com>"

ARG BLACK_VERSION="20.8b1"
ARG PIPENV_VERSION="2020.8.13"
ARG PIPX_VERSION="0.15.5.1"
ARG PYTEST_VERSION="6.1.1"

ENV PATH="/root/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
ENV PIPENV_VENV_IN_PROJECT=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN pip  install "pipx==$PIPX_VERSION"     && \
    pipx install "black==$BLACK_VERSION"   && \
    pipx install "pipenv==$PIPENV_VERSION" && \
    pipx install "pytest==$PYTEST_VERSION"

VOLUME /opt/src

WORKDIR /opt/src

ENTRYPOINT ["/opt/src/entrypoint.sh"]
