FROM alpine:3.7

ENV KUBECTL_VERSION=1.17.0
ENV AWSCLI_VERSION=1.17.14

VOLUME ["/work"]

WORKDIR /work

RUN apk --no-cache update && \
    apk add --no-cache \
    bash=4.4.19-r1 \
    ca-certificates=20190108-r0 \
    git=2.15.4-r0 \
    openssl=1.0.2t-r0 \
    unzip=6.0-r3 \
    curl=7.61.1-r3 \
    make=4.2.1-r0

RUN curl -LO https://storage.googleapis.com/kubernetes-release/release/v${KUBECTL_VERSION}/bin/linux/amd64/kubectl && \
    chmod +x ./kubectl && \
    mv ./kubectl /usr/local/bin/kubectl

RUN apk --no-cache add \
        python=2.7.15-r3 \
        py-pip=9.0.1-r1 \
        py-setuptools=33.1.1-r1 \
        groff=1.22.3-r2 \
        less=520-r0 \
        jq=1.5-r5 \
        gettext-dev=0.19.8.1-r1 \
        g++=6.4.0-r5 \
        zip=3.0-r4 && \
    pip --no-cache-dir install awscli==$AWSCLI_VERSION && \
    update-ca-certificates && \
    rm -rf /var/tmp/ && \
    rm -rf /tmp/* && \
    rm -rf /var/cache/apk/*

# COPY scripts /opt/scripts
# RUN chmod 777 /opt/scripts/*
# ENV PATH "$PATH:/opt/scripts"

ENTRYPOINT [ "kubectl" ]

CMD [ "--version" ]