#文档转换器worker docker文件，主要用于celery的任务调度节点
FROM 10.9.40.181:5000/keda/debian
MAINTAINER shaojj<shaojj@kedachina.com.cn>

ENV TERM xterm

COPY sources.list /etc/apt/sources.list
COPY resolv.conf /etc/resolv.conf
COPY worker/* /opt/spider/

RUN apt-get -yyq update && apt-get install -y python-pip python-dev python-jsonschema
RUN pip install tornado requests celery[redis] motor nose paho-mqtt
RUN mkdir /var/log/celery


WORKDIR /opt/spider
#ENTRYPOINT celery multi start schedule -A schedule -l info -Q default -E -l info --autoscale=6,3 --pidfile=/tmp/%n%I.pid --logfile=/var/log/celery/%n%I.log
