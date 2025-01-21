FROM public.ecr.aws/lambda/provided:al2

# Install Python 3.12
RUN yum install -y gcc openssl-devel bzip2-devel libffi-devel zlib-devel wget make \
    && wget https://www.python.org/ftp/python/3.12.0/Python-3.12.0.tgz \
    && tar xzf Python-3.12.0.tgz \
    && cd Python-3.12.0 \
    && ./configure --enable-optimizations \
    && make altinstall \
    && cd .. \
    && rm -rf Python-3.12.0*

# Set Python 3.12 as the default Python
RUN ln -s /usr/local/bin/python3.12 /usr/bin/python3

# Copy function code
COPY app/ /var/task/
