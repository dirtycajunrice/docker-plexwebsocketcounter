import os
import websocket
from time import sleep
from threading import Thread
from influxdb import InfluxDBClient
from datetime import datetime, timezone

VERSION = "1.1.0"
envars = os.environ

poll_increment = int(envars['POLL_INCREMENT'])
plex_ws = 'ws://{}/:/websockets/notifications'.format(envars['PLEX_URL'])


class PlexWebSocketReader(Thread):
    header = ['X-Plex-Token: {token}'.format(token=envars['PLEX_TOKEN'])]

    def __init__(self):
        Thread.__init__(self)
        self.daemon = True
        self.start()
        self.counter = 0

    def on_message(self, message):
        print(message)
        self.counter += 1

    def on_error(self, error):
        print(error)
        self.counter += 1

    @staticmethod
    def on_close():
        print("### closed ###")

    def run(self):
        websocket.enableTrace(True)
        ws = websocket.WebSocketApp(plex_ws, header=self.header, on_message=self.on_message,
                                    on_error=self.on_error, on_close=self.on_close)
        ws.run_forever()


if __name__ == "__main__":
    reader = PlexWebSocketReader()
    influx = InfluxDBClient(envars['INFLUXDB_URL'], int(envars['INFLUXDB_PORT']),
                            envars['INFLUXDB_USER'], envars['INFLUXDB_PASSWORD'],
                            envars['INFLUXDB_DBNAME'])
    while True:
        sleep(poll_increment)
        avg_requests_per_second = reader.counter / poll_increment
        reader.counter = 0

        influx_payload = [
            {
                "measurement": 'Plex',
                "tags": {
                    "host": "plex",
                },
                "time": datetime.now(timezone.utc).astimezone().isoformat(),
                "fields": {
                    "WS Requests/s": avg_requests_per_second
                }
            }
        ]

        influx.write_points(influx_payload)
