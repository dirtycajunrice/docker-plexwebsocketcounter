FROM amd64/python:3.7.2-alpine

MAINTAINER dirtycajunrice

WORKDIR /app
# Copy the current directory contents into the container at /app
COPY / /app


# Install any needed packages specified in requirements.txt
RUN python3 -m pip install -r /app/requirements.txt

# Define environment variable
ENV INFLUXDB_DBNAME plex
ENV INFLUXDB_URL localhost
ENV INFLUXDB_PORT 8086
ENV POLL_INCREMENT 30
ENV PLEX_URL localhost:32400
ENV PLEX_TOKEN xxxxxxxxxxxxxxxx

# Run app.py when the container launches
CMD ["python", "ws_counter.py"]

