FROM python:3.9-slim-buster

# Set Debian to non interactive
ENV DEBIAN_FRONTEND=noninteractive

# Install & update pkg
RUN echo deb http://http.us.debian.org/debian/ testing non-free contrib main > /etc/apt/sources.list && \
    apt -qq update

RUN apt-get -qq update \
	    && apt-get -qq install -y --no-install-recommends \
	    git g++ gcc autoconf automake aria2 \
	    m4 libtool make libcurl4-openssl-dev \
	    libcrypto++-dev libsqlite3-dev libc-ares-dev \
	    libsodium-dev libnautilus-extension-dev \
	    libssl-dev libfreeimage-dev swig jq ffmpeg git curl \
        p7zip-full p7zip-rar unzip pv locales python3-lxml \
	    && apt-get -y autoremove \
        && apt-get clean \
        && rm -rf /var/lib/apt/lists

# Install Python dependencies
ADD requirements.txt .
RUN pip3 install -U pip wheel setuptools && \
    pip3 install -r requirements.txt

# Set working directory
WORKDIR /app
# Mega sdk
ENV MEGA_SDK_VERSION '3.8.1'
RUN git clone https://github.com/meganz/sdk.git sdk && cd sdk \
    && git checkout v$MEGA_SDK_VERSION \
    && ./autogen.sh && ./configure --disable-silent-rules --enable-python --with-sodium --disable-examples \
    && make -j$(nproc --all) \
    && cd bindings/python/ && python3 setup.py bdist_wheel \
    && cd dist/ && pip3 install --no-cache-dir megasdk-$MEGA_SDK_VERSION-*.whl


# Copy from builder to working directory

COPY extract /usr/local/bin
COPY pextract /usr/local/bin
COPY . /app
RUN chmod +x /usr/local/bin/extract && chmod +x /usr/local/bin/pextract
COPY .netrc /root/.netrc
RUN chmod 600 /app/.netrc && chmod +x aria.sh

# Set command
CMD ["bash", "start.sh"]
