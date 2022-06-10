FROM python:3.9
WORKDIR /work
RUN echo \
    deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bullseye main contrib non-free\
    deb-src https://mirrors.tuna.tsinghua.edu.cn/debian/ bullseye main contrib non-free\
    deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bullseye-updates main contrib non-free\
    deb-src https://mirrors.tuna.tsinghua.edu.cn/debian/ bullseye-updates main contrib non-free\
    deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bullseye-backports main contrib non-free\
    deb-src https://mirrors.tuna.tsinghua.edu.cn/debian/ bullseye-backports main contrib non-free\
    deb https://mirrors.tuna.tsinghua.edu.cn/debian-security bullseye-security main contrib non-free\
    deb-src https://mirrors.tuna.tsinghua.edu.cn/debian-security bullseye-security main contrib non-free\
    > /etc/apt/sources.list
RUN apt-get update
RUN pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple pyparsing tornado scrapy flask pandas flask_cors --no-cache-dir
RUN curl -sL https://deb.nodesource.com/setup_14.x | bash -
RUN apt-get install -y nodejs
RUN npm install -g serve --registry=https://registry.npmmirror.com
RUN apt-get install -y vim
# COPY code /work/
# # CMD cd /work/backend/flask && python3 run.py &
# # CMD cd /work/frontend/
# # CMD serve -s dist &