import logging
import threading
import time
from os.path import exists,getsize
import schedule
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from cachetools import cached, TTLCache
import mapNodes
from db import BaseModel, create_tables

app = Flask(__name__)
api = Api(app)


cache = TTLCache(maxsize=10 ** 9, ttl=120)
log_file_format = "[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s"
main_logger = logging.getLogger('db')
main_logger.setLevel(logging.INFO)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(logging.Formatter(log_file_format))
main_logger.addHandler(console_handler)


class Gateways(Resource):
    def get(self):
        data = self.read_data()
        response = jsonify(data)
        return response

    @cached(cache={})
    def read_data(self):
        data = {}
        db = BaseModel()

        gateways = db.getGateways(intervalHour=2)
        data.update({
            "gateways": gateways,
            "num_gateways": len(gateways),
            "last_update": db.getLastUpdate()['updated_on'],
        })

        return data


def update():
    if not (exists("./data/data.db")) or getsize("./data/data.db") <=0:
        create_tables()

    main_logger.info('Start DB update thread')

    mapping = mapNodes.MapNodes()

    mapping.getGateways()
    schedule.every(2).hours.at("00:00").do(mapping.getGateways)

    while True:
        schedule.run_pending()
        time.sleep(60)


th = threading.Thread(target=update)
th.start()

api.add_resource(Gateways, '/map/gateways')

if __name__ == '__main__':
    host = '0.0.0.0'

    app.run(debug=False, port='8080', host=host)
