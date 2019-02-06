FROM amd64/python:3.7.2-alpine

LABEL maintainer="dirtycajunrice"

WORKDIR /app

COPY /requirements.txt /ws_counter.py /app/

RUN python3 -m pip install -r /app/requirements.txt

ENV INFLUXDB_DBNAME plex
ENV INFLUXDB_URL localhost
ENV INFLUXDB_PORT 8086
ENV POLL_INCREMENT 30
ENV PLEX_URL localhost:32400
ENV PLEX_TOKEN xxxxxxxxxxxxxxxx

# Run app.py when the container launches
CMD ["python3", "ws_counter.py"]

