ARG BUILD_FROM
FROM $BUILD_FROM

ENV LANG C.UTF-8

RUN apk add --no-cache python3
RUN apk add --no-cache py3-pip git wget python3-dev build-base gcc abuild binutils binutils-doc gcc-doc
RUN apk add --update --no-cache python3 py3-pip && ln -sf python3 /usr/bin/python
RUN python3 -m ensurepip
RUN python3 -m pip install --no-cache --upgrade pip setuptools websockets pykodi
# RUN python3 -m pip install git+https://github.com/OnFreund/PyKodi

WORKDIR /data

COPY kodi2home.py /
RUN chmod a+x /kodi2home.py
# Copy data for add-on
COPY run.sh /
RUN chmod a+x /run.sh

CMD [ "/run.sh" ]
