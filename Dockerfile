FROM python:3.9.0-buster

LABEL "maintainer" = "Egon Braun <egon@mundoalem.io>"

ARG USER_ID
ARG GROUP_ID

ENV PATH="/home/developer/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN addgroup --gid $GROUP_ID developer
RUN adduser --disabled-password --gecos '' --uid $USER_ID --gid $GROUP_ID developer

USER developer

RUN mkdir /home/developer/src

WORKDIR /home/developer/src

RUN pip  install "pipx==0.15.6.0"
RUN pipx install "black==20.8b1"
RUN pipx install "poetry==1.1.4"
RUN pipx install "pytest==6.1.2"

COPY --chown=developer:developer . /home/developer/src

RUN poetry install --remove-untracked --no-root --ansi
RUN poetry run pip freeze > requirements.txt
RUN pip install -r requirements.txt

VOLUME /home/developer/src

CMD ["/home/developer/src/entrypoint.sh"]
