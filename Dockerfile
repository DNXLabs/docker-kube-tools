FROM alpine:3.12

ENV KUBECTL_VERSION=1.18.0
ENV AWSCLI_VERSION=1.17.14

VOLUME ["/work"]

WORKDIR /work

RUN apk --no-cache update && \
    apk --no-cache add \
        bash=5.0.17-r0 \
        ca-certificates=20191127-r4 \
        git=2.26.2-r0 \
        openssl=1.1.1i-r0 \
        unzip=6.0-r8 \
        curl=7.69.1-r3 \
        make=4.3-r0 \
        tar=1.32-r1 \
        python3=3.8.5-r0 \
        py-pip=20.1.1-r0 \
        py-setuptools=47.0.0-r0 \
        groff=1.22.4-r1 \
        less=551-r0 \
        jq=1.6-r1 \
        gettext-dev=0.20.2-r0 \
        g++=9.3.0-r2 \
        zip=3.0-r8 && \
    python3 -m pip install --upgrade pip==20.3.3 && \
    python3 -m pip --no-cache-dir install awscli==$AWSCLI_VERSION && \
    update-ca-certificates && \
    rm -rf /var/tmp/ && \
    rm -rf /tmp/* && \
    rm -rf /var/cache/apk/*

# Kubectl
RUN curl -LO https://storage.googleapis.com/kubernetes-release/release/v${KUBECTL_VERSION}/bin/linux/amd64/kubectl && \
    chmod +x ./kubectl && \
    mv ./kubectl /usr/local/bin/kubectl

# Helm
RUN curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3 && \
    chmod 700 get_helm.sh && \
    ./get_helm.sh

# Velero
RUN curl -LO https://github.com/vmware-tanzu/velero/releases/download/v1.5.3/velero-v1.5.3-linux-amd64.tar.gz && \
    tar -xvzf velero-v1.5.3-linux-amd64.tar.gz && \
    chmod +x ./velero-v1.5.3-linux-amd64/velero && \
    mv ./velero-v1.5.3-linux-amd64/velero /usr/local/bin/velero && \
    rm -rf ./velero-v1.5.3-linux-amd64