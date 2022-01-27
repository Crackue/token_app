FROM python:3.9-buster
ARG BOT_TOKEN
ARG TELEGRAM_URL
ARG WEB_HOOK_URL

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV APP_HOME=/bot_service
ENV ENV_PATH=.env.dev
ENV ETHER_SERVICE_HOST=etherservice
ENV USER_SERVICE_HOST=userservice
WORKDIR $APP_HOME
COPY requirements.txt $APP_HOME/requirements.txt
RUN pip3 install --upgrade pip
RUN pip3 install --upgrade certifi
RUN pip3 install -r requirements.txt
COPY . $APP_HOME
CMD gunicorn bot_service.wsgi:application --bind 0.0.0.0:8002
