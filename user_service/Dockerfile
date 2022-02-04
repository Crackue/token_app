FROM python:3.9-buster
ARG DB_NAME
ARG DB_USER
ARG DB_PASSWORD
ARG DB_HOST
ARG ETHER_SERVICE_HOST

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV APP_HOME=/user_service
ENV ENV_PATH=.env.dev
ENV ETHER_SERVICE_HOST=etherservice
ENV PORT=8000
WORKDIR $APP_HOME
COPY requirements.txt $APP_HOME/requirements.txt
RUN pip3 install --upgrade pip
RUN pip3 install --upgrade certifi
RUN pip3 install -r requirements.txt
COPY . $APP_HOME
CMD gunicorn user_service_project.wsgi:application --bind 0.0.0.0:$PORT
