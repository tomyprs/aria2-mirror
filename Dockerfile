FROM ghcr.io/tomyprs/aria2-mirror:master

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