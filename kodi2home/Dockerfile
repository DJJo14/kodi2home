ARG BUILD_FROM
FROM $BUILD_FROM

ENV LANG C.UTF-8

RUN apk add --no-cache python3 py3-pip git wget python3-dev build-base gcc abuild binutils binutils-doc gcc-doc
RUN apk add --update --no-cache python3 py3-pip && ln -sf python3 /usr/bin/python 
#&& python3 -m ensurepip was after this but did not work because of this https://stackoverflow.com/questions/75608323/how-do-i-solve-error-externally-managed-environment-every-time-i-use-pip-3
RUN python3 -m pip install --no-cache --break-system-packages --upgrade pip setuptools websockets pykodi async-timeout
# RUN python3 -m pip install git+https://github.com/OnFreund/PyKodi

WORKDIR /data

COPY kodi2home.py /
RUN chmod a+x /kodi2home.py
# Copy data for add-on
COPY run.sh /
RUN chmod a+x /run.sh

CMD [ "/run.sh" ]
