FROM alpine:latest

RUN echo "@testing http://dl-4.alpinelinux.org/alpine/edge/testing" >> /etc/apk/repositories \
  && apk add --update \
              musl \
              build-base \
              bash \
              git \
              python \
              python-dev \
              py-psutil \
              py-requests \
              py-pip \
  && pip install --upgrade pip \
  && rm /var/cache/apk/*

# make some useful symlinks that are expected to exist
RUN cd /usr/bin \
  && ln -sf easy_install-2.7 easy_install \
  && ln -sf python2.7 python \
  && ln -sf python2.7-config python-config \
&& ln -sf pip2.7 pip
RUN pip install python-daemon
RUN mkdir -p /opt/monslack
RUN mkdir -p /etc/monslack/
ADD monitor.py /opt/monslack/
#ADD config.json /etc/monslack/
ENTRYPOINT ["python", "/opt/monslack/monitor.py"]

