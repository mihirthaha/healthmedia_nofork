FROM docker.io/python:3.11
WORKDIR /
RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y python3 python3-pip git
COPY . /
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn
ENV GUNICORN_CMD_ARGS="--workers=1 --bind=0.0.0.0:8505"
EXPOSE 8505
ENV FLASK_ENV=production
CMD [ "gunicorn", "main:app" ]