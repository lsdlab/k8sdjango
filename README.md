# k8sdjango 

Django 项目 Docker 部署示例，postgresql 配置映射到容器中，修改成可远程连接，nginx/gunicorn 日志映射到宿主机器，postgresql/redis/rabbitmq 容器数据持久化，映射 volume 到宿主机，ADMIN 的静态文件映射到宿主机器。


## docker-compose 启动

```
docker-compose build
docker-compose up
```


## 组件

- python 3.7.4
- postgresql 11.4
- redis 5.0.5
- rabbitmq 3.7.17 with management web UI
- nginx 1.16
- djangorestframework
- celery


## 端口占用

- nginx 8080
- postgresql 5432 可远程连接
- redis 6379 不可远程连接
- rabbitmq 5672/15672(management web UI可使用)


## ROADMAP

- [x] celery broker 换成 rabbitmq
- [x] nginx/gunicorn 日志映射出来
- [x] docker swarm 集群部署
- [ ] k8s 集群部署
