FROM lzzy12/mega-sdk-python:latest

WORKDIR /app

RUN apt-get -qq update && \
    apt-get install -y software-properties-common && \
    rm -rf /var/lib/apt/lists/* && \
    apt-add-repository non-free && \
    apt-get -qq update && \
    apt-get -qq install -y git python3 python3-pip \
        unzip p7zip-full p7zip-rar \
        aria2 \
        curl pv jq \
        ffmpeg locales \
        python3-lxml && \
    apt-get purge -y software-properties-common

COPY requirements.txt .

COPY extract /usr/local/bin
RUN chmod +x /usr/local/bin/extract

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x aria.sh

CMD ["bash","start.sh"]
