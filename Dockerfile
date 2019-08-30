FROM python:3.7

ARG TEMPDIR=/tmp/routeros-update-check
ENV TEMPDIR=${TEMPDIR}

COPY . ${TEMPDIR}
WORKDIR ${TEMPDIR}
RUN python setup.py install \
  && rm -rf ${TEMPDIR}

ARG DOWNLOAD_DIR=/downloads
ARG USERNAME=update_checker
ENV USERNAME=${USERNAME} DOWNLOAD_DIR=${DOWNLOAD_DIR}

RUN mkdir -p ${DOWNLOAD_DIR} \
  && useradd -MU -s /bin/bash ${USERNAME} \
  && chown -R ${USERNAME}:${USERNAME} ${DOWNLOAD_DIR}

VOLUME ${DOWNLOAD_DIR}
USER ${USERNAME}
WORKDIR ${DOWNLOAD_DIR}

ENTRYPOINT ["/usr/local/bin/ros-updates"]
CMD ["--help"]
