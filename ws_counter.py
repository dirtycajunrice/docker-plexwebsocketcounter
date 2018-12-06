import os
import socket
import websocket
from time import sleep
from threading import Thread
from influxdb import InfluxDBClient
from datetime import datetime, timezone

vars = os.environ

poll_increment = int(vars['POLL_INCREMENT'])
plex_ws = 'ws://{}/:/websockets/notifications'.format(vars['PLEX_URL'])

class PlexWebSocketReader(Thread):
    header = ['X-Plex-Token: {token}'.format(token=vars['PLEX_TOKEN'])]

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

    def on_close(self):
        print("### closed ###")

    def run(self):
        websocket.enableTrace(True)
        ws = websocket.WebSocketApp(plex_ws, header=self.header, on_message=self.on_message,
                                    on_error=self.on_error, on_close=self.on_close)
        ws.run_forever()


if __name__ == "__main__":
    reader = PlexWebSocketReader()
    influx = InfluxDBClient(vars['INFLUXDB_URL'], int(vars['INFLUXDB_PORT']), 'root', 'root', vars['INFLUXDB_DBNAME'])
    while True:
        sleep(poll_increment)
        avg_requests_per_second = reader.counter / poll_increment
        reader.counter = 0

        influx_payload = [
            {
                "measurement": "Plex Info",
                "tags": {
                    "host": socket.gethostname(),
                },
                "time": datetime.now(timezone.utc).astimezone().isoformat(),
                "fields": {
                    "WS Requests/s": avg_requests_per_second
                }
            }
        ]

        influx.write_points(influx_payload)
