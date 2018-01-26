# 开启MongoDB服务

FROM 10.9.40.181:5000/keda/debian:latest
MAINTAINER YuexLi

ENV LANG en_US.UTF-8
ENV TERM xterm

COPY sources.list /etc/apt/sources.list
COPY resolv.conf /etc/resolv.conf
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

RUN /bin/echo 'root:kedakeda' |chpasswd
RUN apt-get -yyq update && apt-get -yy install nginx-extras

WORKDIR /home
