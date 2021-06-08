FROM python:3-slim-buster

# Set Debian to non interactive
ENV DEBIAN_FRONTEND=noninteractive

# Install & update pkg
RUN apt-get -qq update && \
    apt-get install -y software-properties-common && \
    rm -rf /var/lib/apt/lists/* && \
    apt-add-repository non-free && \
    apt-get -qq update

RUN apt-get -qq update \
	    && apt-get -qq install -y --no-install-recommends \
	    git g++ gcc autoconf automake aria2 \
	    m4 libtool qt4-qmake make libqt4-dev libcurl4-openssl-dev \
	    libcrypto++-dev libsqlite3-dev libc-ares-dev \
	    libsodium-dev libnautilus-extension-dev \
	    libssl-dev libfreeimage-dev swig jq ffmpeg git curl \
        p7zip-full p7zip-rar unzip pv locales python3-lxml \
	    && apt-get -y autoremove

# Installing mega sdk python binding
ENV MEGA_SDK_VERSION '3.8.1'
RUN git clone https://github.com/meganz/sdk.git sdk && cd sdk \
    && git checkout v$MEGA_SDK_VERSION \
    && ./autogen.sh && ./configure --disable-silent-rules --enable-python --with-sodium --disable-examples \
    && make -j$(nproc --all) \
    && cd bindings/python/ && python3 setup.py bdist_wheel \
    && cd dist/ && pip3 install --no-cache-dir megasdk-$MEGA_SDK_VERSION-*.whl

# Install Python dependencies
ADD requirements.txt .
RUN pip3 install -U pip wheel setuptools && \
    pip3 install -r requirements.txt

# Set working directory
WORKDIR /app

# Copy from builder to working directory
COPY . /app

# Set command 
CMD ["bash", "start.sh"]