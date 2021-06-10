# Use own Docker image
FROM thekai/aria-megasdk:latest

RUN apt-get -qq install libssl-dev libcrypto++-dev

# Install Python dependencies
ADD requirements.txt .
RUN pip3 install -U pip wheel setuptools && \
    pip3 install -r requirements.txt

# Set working directory
WORKDIR /app

# Copy from builder to working directory
COPY extract /usr/local/bin
COPY pextract /usr/local/bin
COPY . /app
RUN chmod +x /usr/local/bin/extract && chmod +x /usr/local/bin/pextract
COPY .netrc /root/.netrc
RUN chmod 600 /app/.netrc && chmod +x aria.sh

# Set command
CMD ["bash", "start.sh"]
