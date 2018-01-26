# 开启MongoDB服务

FROM 10.9.40.181:5000/keda/debian:latest
MAINTAINER YuexLi

ENV LANG en_US.UTF-8
ENV LC_ALL C
ENV TERM xterm

COPY sources.list /etc/apt/sources.list
COPY resolv.conf /etc/resolv.conf
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY modpasswd.sh /usr/bin/

RUN /bin/echo 'root:kedakeda' |chpasswd \
    && apt-get -yyq update && apt-get -yy install mongodb
    && sed -i -e "s/bind_ip = 127.0.0.1/bind_ip = 0.0.0.0/g" /etc/mongodb.conf
    && sed -i -e "s/\#auth = true/auth = true/g" /etc/mongodb.conf
    && sed -i -e "s/\#port = 27017/port = 27017/g" /etc/mongodb.conf
    && chown mongodb:mongodb /var/log/mongodb/ -R
    && chown mongodb:mongodb /var/lib/mongodb/ -R
    && chown mongodb:mongodb /etc/mongodb.conf
    && /etc/init.d/mongodb start && /usr/bin/modpasswd.sh
    && rm /usr/bin/modpasswd.sh

WORKDIR /home
