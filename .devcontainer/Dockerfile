FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive

RUN \
    apt-get update && \
    apt-get -y install \
        --no-install-recommends \
        locales \
        curl \
        make \
        git \
        python3-dev \
        python3-pip \
        python3-venv \
        python3-wheel \
    && \
    rm -rf /var/lib/apt/lists/*


# Add non-root user
ARG USERNAME=nonroot
RUN groupadd --gid 1000 $USERNAME && \
    useradd --uid 1000 --gid 1000 -m $USERNAME

## Make sure to reflect new user in PATH
ENV PATH="/home/${USERNAME}/.local/bin:${PATH}"
USER $USERNAME



RUN pip install --upgrade pip


COPY --chown=nonroot:1000 requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt && \
    rm /tmp/requirements.txt