# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2021-present Kaleidos INC

#использование базового образа пайтон
FROM python:3.11-slim
#просто владельцы образа, контактное лицо
LABEL maintainer="support@taiga.io"

# Настройка локалей
#RUN apt-get update && apt-get upgrade -y && \
    #apt-get install -y sudo locales && \
    #rm -rf /var/lib/apt/lists/* && \
    #localedef -i en_US -c -f UTF-8 -A /usr/share/locale/locale.alias en_US.UTF-8



#ENV LANG=en_US.utf8
ENV DEBIAN_FRONTEND=noninteractive

# Установка Python и необходимых инструментов
#RUN apt-get update && \
    #apt-get install -y python3 python3-pip python3-venv && \
    #python3 -m venv /opt/venv && \
    #rm -rf /var/lib/apt/lists/*

# Переключение на виртуальное окружение Python
#ENV PATH="/opt/venv/bin:$PATH"
#отключает буферизацию вывода, чтобы логи сразу писались в консоль
ENV PYTHONUNBUFFERED=1
#предотвращает создание файлов *.pyc.
ENV PYTHONDONTWRITEBYTECODE=1
#включает вывод стектрейсов для ошибок в Python.
ENV PYTHONFAULTHANDLER=1

# Use a virtualenv
#Создание виртуального окружения, только внутри докера
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Get the code, копирование кода и сохранение на путь (вторая строчка)
COPY . /taiga-back
WORKDIR /taiga-back

# grab gosu for easy step-down from root (типа для перехода)
# https://github.com/tianon/gosu/blob/master/INSTALL.md
ENV GOSU_VERSION 1.12

# установка зависимостей системы(библиотеки, инструменты)
RUN set -eux; \
    apt-get update; \
    # install system dependencies
    apt-get install -y \
       build-essential \
       gettext \
       # libpq5 needed in runtime for psycopg2
       libpq5 \
       # для работы с PostgreSQL через psycopg2
       libpq-dev \
       git \
       net-tools \
       procps \
       wget; \
    # install gosu
    apt-get install -y --no-install-recommends ca-certificates wget; \
    dpkgArch="$(dpkg --print-architecture | awk -F- '{ print $NF }')"; \
    wget -O /usr/local/bin/gosu "https://github.com/tianon/gosu/releases/download/$GOSU_VERSION/gosu-$dpkgArch"; \
	wget -O /usr/local/bin/gosu.asc "https://github.com/tianon/gosu/releases/download/$GOSU_VERSION/gosu-$dpkgArch.asc"; \
    chmod +x /usr/local/bin/gosu; \
    # verify gosu signature
    export GNUPGHOME="$(mktemp -d)"; \
	gpg --batch --keyserver hkps://keys.openpgp.org --recv-keys B42F6819007F00F88E364FD4036A9C25BF357DD4; \
	gpg --batch --verify /usr/local/bin/gosu.asc /usr/local/bin/gosu; \
	command -v gpgconf && gpgconf --kill all || :; \
	rm -rf "$GNUPGHOME" /usr/local/bin/gosu.asc; \
    # install Taiga dependencies
    #обновляем pip
    python -m pip install --upgrade pip; \
    # пакет wheel, который нужен для правильной сборки некоторых зависимостей
    python -m pip install wheel; \
    python -m pip install -r requirements.txt; \
    python -m pip install -r requirements-contribs.txt; \
    # Эти команды собирают переводы и собирают статические файлы проекта, которые используются для фронтенда.
    python manage.py compilemessages; \
    python manage.py collectstatic --no-input; \
    chmod +x docker/entrypoint.sh; \
    chmod +x docker/async_entrypoint.sh; \
    cp docker/config.py settings/config.py; \
    #  create taiga group and user to use it and give permissions over the code (in entrypoint)
    groupadd --system taiga --gid=999; \
    useradd --system --no-create-home --gid taiga --uid=999 --shell=/bin/bash taiga; \
    mkdir -p /taiga-back/media/exports; \
    chown -R taiga:taiga /taiga-back; \
    # remove unneeded files and packages
    apt-get purge -y \
       build-essential \
       gettext \
       git \
       libpq-dev \
       net-tools \
       procps \
       wget; \
    apt-get autoremove -y; \
    rm -rf /var/lib/apt/lists/*; \
    rm -rf /root/.cache; \
    # clean taiga
    rm requirements.txt; \
    rm requirements-contribs.txt; \
    find . -name '__pycache__' -exec rm -r '{}' +; \
    find . -name '*pyc' -exec rm -r '{}' +; \
    find . -name '*po' -exec rm -r '{}' +

# Установка зависимостей
#RUN pip install --upgrade pip && \
    #pip install wheel && \
    #pip install -r requirements.txt && \
    #pip install -r requirements-contribs.txt && \
    #python manage.py compilemessages && \
    #python manage.py collectstatic --no-input

# Создание пользователя для контейнера
#RUN groupadd --system taiga --gid=999 && \
    #useradd --system --no-create-home --gid taiga --uid=999 --shell=/bin/bash taiga && \
    #mkdir -p /taiga-back/media/exports && \
    #chown -R taiga:taiga /taiga-back

ENV DJANGO_SETTINGS_MODULE=settings.config

EXPOSE 8000
ENTRYPOINT ["./docker/entrypoint.sh"]
