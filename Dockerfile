# Use own Docker image
FROM thekai/aria-megasdk:latest

RUN apt-get -qq install libssl-dev libcrypto++-dev openssl

# Install Python dependencies
ADD requirements.txt .
RUN pip3 install -U pip wheel setuptools && \
    pip3 install -r requirements.txt

# Set working directory
WORKDIR /app

# Copy to working dir
COPY . /app
RUN set -ex \
    && chmod 777 /app \
    && cp netrc /root/.netrc \
    && cp extract pextract /usr/local/bin \
    && chmod +x aria.sh /usr/local/bin/extract /usr/local/bin/pextract

# Set command
CMD ["bash", "start.sh"]
