FROM python:3.9-buster
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV APP_HOME=/ether_service
ENV ENV_PATH=.env.dev
WORKDIR $APP_HOME
COPY requirements.txt $APP_HOME/requirements.txt
RUN pip3 install --upgrade pip
RUN pip3 install eth-brownie
RUN pip3 install -r requirements.txt
COPY . $APP_HOME
