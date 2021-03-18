FROM python:3.9.2-alpine3.13

ENV appDir=/app

ADD ./app ${appDir}

WORKDIR ${appDir}

RUN pip3 install -r requirements.txt

EXPOSE 5000

ENTRYPOINT [ "python3", "index.py" ]