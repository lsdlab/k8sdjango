FROM python:3.7.4-alpine3.10 as build1
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE conf.production.settings
ENV TZ Asia/Shanghai
RUN mkdir /k8sdjango

# add china mirrors
RUN echo 'http://mirrors.aliyun.com/alpine/v3.10/community/'>/etc/apk/repositories
RUN echo 'http://mirrors.aliyun.com/alpine/v3.10/main/'>>/etc/apk/repositories

# install psycopg2-binary
RUN apk update \
    && apk add tzdata \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add postgresql-dev \
    && pip install -U pip setuptools -i https://mirrors.aliyun.com/pypi/simple/ \
    && pip install psycopg2-binary -i https://mirrors.aliyun.com/pypi/simple/ \
    && apk del build-deps

# install requirements and copy code
COPY requirements.txt /k8sdjango
RUN pip install -r /k8sdjango/requirements.txt -i https://mirrors.aliyun.com/pypi/simple/

FROM python:3.7.4-alpine3.10
COPY --from=build1 / /
COPY . /k8sdjango
WORKDIR /k8sdjango
COPY ./wait-for /bin/wait-for
