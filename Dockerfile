# Mesma receita de ghcr.io/r4kashy/mta-box64:latest.
# A base passou de Debian 12 (bookworm, glibc 2.36) para Debian 13 (trixie, glibc 2.41).
# Os nomes que o Debian trocou: libicu72 -> libicu76, libzip4 -> libzip5, libfontconfig -> libfontconfig1.
FROM --platform=linux/arm64 debian:trixie-slim

LABEL author="r4kashy" maintainer="r4kashy"
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
 && apt-get upgrade -y \
 && apt-get install -y --no-install-recommends \
    libc++-dev \
    libc6 \
    git \
    wget \
    curl \
    tar \
    zip \
    unzip \
    binutils \
    xz-utils \
    liblzo2-2 \
    cabextract \
    iproute2 \
    net-tools \
    libatomic1 \
    libsdl1.2debian \
    libsdl2-2.0-0 \
    libfontconfig1 \
    libicu76 \
    icu-devtools \
    libunwind8 \
    libssl-dev \
    sqlite3 \
    libsqlite3-dev \
    libmariadb-dev \
    libmariadb-dev-compat \
    libduktape207 \
    locales \
    ffmpeg \
    gnupg2 \
    apt-transport-https \
    ca-certificates \
    libz3-dev \
    rapidjson-dev \
    tzdata \
    libevent-dev \
    libzip5 \
    libsdl2-mixer-2.0-0 \
    libsdl2-image-2.0-0 \
    build-essential \
    cmake \
    libgdiplus \
    libstdc++6 \
 && sed -i 's/^# *\(en_US.UTF-8 UTF-8\)/\1/' /etc/locale.gen \
 && locale-gen \
 && update-locale lang=en_US.UTF-8 \
 && dpkg-reconfigure --frontend noninteractive locales \
 && wget https://ryanfortner.github.io/box64-debs/box64.list -O /etc/apt/sources.list.d/box64.list \
 && wget -qO- https://ryanfortner.github.io/box64-debs/KEY.gpg | gpg --dearmor -o /etc/apt/trusted.gpg.d/box64-debs-archive-keyring.gpg \
 && apt-get update \
 && apt-get install -y box64-rpi4arm64 \
 && useradd -d /home/container -m container \
 && dpkg --add-architecture amd64 \
 && printf '%s\n' 'deb [arch=amd64] http://deb.debian.org/debian trixie main' > /etc/apt/sources.list.d/amd64.list \
 && printf '%s\n' 'deb [arch=amd64] http://deb.debian.org/debian-security trixie-security main' >> /etc/apt/sources.list.d/amd64.list \
 && apt-get update \
 && apt-get install -y --no-install-recommends libncursesw6:amd64 libtinfo6:amd64 \
 && rm -rf /var/lib/apt/lists/*

COPY entrypoint.sh /entrypoint.sh

USER container
ENV USER=container
ENV HOME=/home/container
WORKDIR /home/container

CMD ["/bin/bash", "/entrypoint.sh"]
