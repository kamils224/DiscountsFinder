FROM python:3.9.7-slim-buster as web
WORKDIR /discounts_finder

# Requirements for chromium
RUN apt-get update && apt install -y gconf-service libasound2 libatk1.0-0 libc6 \
    libcairo2 libcups2 libdbus-1-3 libexpat1 libfontconfig1 libgcc1 \
    libgconf-2-4 libgdk-pixbuf2.0-0 libglib2.0-0 libgtk-3-0 libnspr4 \
    libpango-1.0-0 libpangocairo-1.0-0 libstdc++6 libx11-6 libx11-xcb1 libxcb1 \
    libxcomposite1 libxcursor1 libxdamage1 libxext6 libxfixes3 libxi6 libxrandr2 \
    libxrender1 libxss1 libxtst6 ca-certificates fonts-liberation libappindicator1 \
    libnss3 lsb-release xdg-utils wget

RUN pip install pyppeteer && pyppeteer-install

COPY requirements.txt /discounts_finder/requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

ENV PYTHONPATH="$PYTHONPATH:/"

ADD . /discounts_finder
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
############################################################
FROM web as celery_worker
CMD ["celery", "-A", "celery_worker.celery_init.celery", "worker", "-l", "info"]
############################################################
FROM celery_worker as celery_beat
CMD ["celery", "-A", "celery_worker.celery_init.celery", "beat", "-l", "info"]
