FROM ubuntu:18.04

WORKDIR /app
RUN apt-get -qq update
RUN apt-get -qq install -y aria2 git python3 python3-pip rar unzip \
    locales python3-lxml \
    curl pv jq ffmpeg
COPY requirements.txt .
COPY extract /usr/local/bin
RUN chmod +x /usr/local/bin/extract
RUN pip3 install --no-cache-dir -r requirements.txt

RUN locale-gen en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8
COPY . .

RUN chmod +x aria.sh

CMD ["bash","start.sh"]
