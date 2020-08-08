FROM lzzy12/mega-sdk-python:latest

WORKDIR /app

RUN apt-get -qq update
RUN apt-get -qq install -y aria2 git python3 python3-pip \
    unzip p7zip-full \
    locales python3-lxml \
    curl pv jq ffmpeg

COPY requirements.txt .

COPY extract /usr/local/bin
RUN chmod +x /usr/local/bin/extract

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x aria.sh

CMD ["bash","start.sh"]
