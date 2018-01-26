# 开启MongoDB服务

FROM 10.9.40.181:5000/keda/mysql:5.5
MAINTAINER YuexLi

ENV LANG en_US.UTF-8
ENV TERM xterm

COPY sources.list /etc/apt/sources.list
COPY resolv.conf /etc/resolv.conf
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

RUN /bin/echo 'root:kedakeda' |chpasswd

WORKDIR /home
ENTRYPOINT ["/usr/bin/supervisord"]
