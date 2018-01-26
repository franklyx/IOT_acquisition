# 开启MongoDB服务

FROM python:latest
MAINTAINER YuexLi

ENV LANG en_US.UTF-8
ENV TERM xterm

COPY resolv.conf /etc/resolv.conf
COPY sources.list /etc/apt/sources.list

# 创建程序运行空间
RUN mkdir -p /home/code
WORKDIR /home/code

# 安装依赖
COPY requirements.txt /home/code
RUN pip install -r requirements.txt

ENTRYPOINT ["python","server.py"]
