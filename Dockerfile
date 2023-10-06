FROM ubuntu:22.04

ARG CHROME_BINARY_PATH="/usr/bin"
ENV PY_VERSION $PY_VERSION

RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
     && apt-get -y install --no-install-recommends \
        build-essential \
        libpython3-dev \
        python3 \
        python3-pip \
        python3-wheel \
        python3-dev \
        python3-venv \
        software-properties-common \
        wget \
        unzip \
        jq \
        curl \
    && wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && apt-get -f install \
    && apt-get install libappindicator1 fonts-liberation dbus-x11 xfonts-base xfonts-100dpi xfonts-75dpi xfonts-cyrillic xfonts-scalable libxss1 lsb-release xdg-utils libasound2 libgbm1 libnspr4 libnss3 libu2f-udev libatk-bridge2.0-0 libatspi2.0-0 libgtk-3-0 libxkbcommon0 libvulkan1 -y \
    && dpkg -i google-chrome-stable_current_amd64.deb \
    && apt-get -f install \
    && JSON_RESPONSE=$(curl -s "https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json") \
    && CHROME_VERSION=$(echo $JSON_RESPONSE | jq -r '.channels.Stable.version') \
    && wget --no-verbose -O /tmp/chromedriver_linux64.zip https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/$CHROME_VERSION/linux64/chromedriver-linux64.zip \
    && unzip /tmp/chromedriver_linux64.zip \
    && mv chromedriver-linux64/chromedriver ${CHROME_BINARY_PATH}/chromedriver \
    && chown root:root ${CHROME_BINARY_PATH}/chromedriver \
    && chmod +x ${CHROME_BINARY_PATH}/chromedriver \
    && apt-get update && apt-get -y upgrade

COPY requirements.txt .

RUN pip3 install -U pip setuptools==45.2.0 wheel \
    && pip3 install --no-cache-dir -r requirements.txt

COPY . .
#CMD ["/bin/bash", "-c", "python3 selenium_sadness.py"]
