FROM alpine:3.7

ENV KUBECTL_VERSION=1.17.0
ENV AWSCLI_VERSION=1.17.14

VOLUME ["/work"]

WORKDIR /work

RUN apk update && \
    apk add bash ca-certificates git openssl unzip curl make && \
    cd /tmp && \
    curl -LO https://storage.googleapis.com/kubernetes-release/release/v${KUBECTL_VERSION}/bin/linux/amd64/kubectl && \
    chmod +x ./kubectl && \
    mv ./kubectl /usr/local/bin/kubectl


RUN apk --no-cache add python py-pip py-setuptools groff less jq gettext-dev curl wget g++ zip && \
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