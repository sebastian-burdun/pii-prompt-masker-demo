FROM python:3.13.0-bookworm

# install scrubadub_stanford dependencies
RUN apt update && apt install default-jdk -y

# install scrubadub_address dependencies
RUN apt install curl autoconf automake libtool pkg-config -y && \
    git clone https://github.com/openvenues/libpostal && \
    cd libpostal && \
    ./bootstrap.sh && \
    ./configure --datadir=/opt/libpostal_data && \
    make -j4 && \
    make install && \
    ldconfig

COPY requirements.txt .
RUN pip install -r requirements.txt

WORKDIR /app
COPY app/ .
