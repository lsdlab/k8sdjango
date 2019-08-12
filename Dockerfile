FROM python:3.7.4-alpine3.10
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE conf.production.settings
RUN mkdir /k8sdjango
COPY . /k8sdjango
WORKDIR /k8sdjango

# add china mirrors
RUN echo 'http://mirrors.aliyun.com/alpine/v3.10/community/'>/etc/apk/repositories
RUN echo 'http://mirrors.aliyun.com/alpine/v3.10/main/'>>/etc/apk/repositories

# install psycopg2-binary
RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add postgresql-dev \
    && pip install --upgrade pip setuptools \
    && pip install psycopg2-binary -i https://mirrors.aliyun.com/pypi/simple/ \
    && apk del build-deps

# install requirements and copy code
RUN pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/
