# 开启MongoDB服务

FROM 10.9.40.181:5000/keda/emqtt:latest
MAINTAINER YuexLi

ENV LANG en_US.UTF-8
ENV TERM xterm

COPY sources.list /etc/apt/sources.list
COPY resolv.conf /etc/resolv.conf

RUN /bin/echo 'root:kedakeda' |chpasswd
RUN echo 'auth.user.1.username = admin' >> /etc/emqttd/plugins/emq_auth_username.conf
RUN echo 'auth.user.1.password = admin' >> /etc/emqttd/plugins/emq_auth_username.conf
RUN /etc/init.d/emqttd start && emqttd_ctl plugins load emq_auth_username && emqttd_ctl users add admin admin

WORKDIR /home
