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
RUN mkdir -p /opt/monslack/checks
ADD requirements.txt /opt/monslack/
RUN pip install -r /opt/monslack/requirements.txt
RUN mkdir -p /etc/monslack/
ADD run_monitor.py /opt/
ADD monslack/monitor.py /opt/monslack/
ADD monslack/__init__.py /opt/monslack/
ADD monslack/checks/__init__.py /opt/monslack/checks/
ADD monslack/checks/DiskCheck.py /opt/monslack/checks/
ADD monslack/checks/CPUCheck.py /opt/monslack/checks/
ADD monslack/checks/LogCheck.py /opt/monslack/checks/
ADD monslack/checks/MemoryCheck.py /opt/monslack/checks/
#ADD config.json /etc/monslack/
ENTRYPOINT ["python", "/opt/run_monitor.py", "start"]

