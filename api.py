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
from utils import Utils

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


class GatewaysAS(Resource):
    def get(self):
        data = self.read_data()
        response = jsonify(data)
        return response

    @cached(cache={})
    def read_data(self):
        data = {}
        db = BaseModel()

        response = db.getGatewaysAS(intervalHour=Utils.GATEWAY_LAST_UPDATE_HOUR)
        data.update({
            "asn": response,
            "num_uniq_asn": len(response),
            "last_update": db.getLastUpdate()['updated_on'],
        })

        return data
class GatewaysOrg(Resource):
    def get(self):
        data = self.read_data()
        response = jsonify(data)
        return response

    @cached(cache={})
    def read_data(self):
        data = {}
        db = BaseModel()

        response = db.getGatewaysOrg(intervalHour=Utils.GATEWAY_LAST_UPDATE_HOUR)
        data.update({
            "orgs": response,
            "num_uniq_org": len(response),
            "last_update": db.getLastUpdate()['updated_on'],
        })

        return data
class GatewaysCountries(Resource):
    def get(self):
        data = self.read_data()
        response = jsonify(data)
        return response

    @cached(cache={})
    def read_data(self):
        data = {}
        db = BaseModel()

        countries = db.getGatewaysCountry(intervalHour=Utils.GATEWAY_LAST_UPDATE_HOUR)
        data.update({
            "countries": countries,
            "num_uniq_countries": len(countries),
            "last_update": db.getLastUpdate()['updated_on'],
        })

        return data

class GatewaysContinent(Resource):
    def get(self):
        data = self.read_data()
        response = jsonify(data)
        return response

    @cached(cache={})
    def read_data(self):
        data = {}
        db = BaseModel()

        continents = db.getGatewaysContinents(intervalHour=Utils.GATEWAY_LAST_UPDATE_HOUR)
        data.update({
            "continents": continents,
            "num_uniq_countries": len(continents),
            "num_gateways": db.getNumGateways(),
            "last_update": db.getLastUpdate()['updated_on'],
        })

        return data

class Gateways(Resource):
    def get(self):
        data = self.read_data()
        response = jsonify(data)
        return response

    @cached(cache={})
    def read_data(self):
        data = {}
        db = BaseModel()

        gateways = db.getGateways(intervalHour=Utils.GATEWAY_LAST_UPDATE_HOUR)
        data.update({
            "gateways": gateways,
            "num_gateways": len(gateways),
            "last_update": db.getLastUpdate()['updated_on'],
        })

        return data


def update():
    if not (exists("./data/data.db")) or getsize("./data/data.db") <= 0:
        create_tables()

    main_logger.info('Start DB update thread')

    mapping = mapNodes.MapNodes()
    Utils.updateGeoIP()

    mapping.getGateways()
    schedule.every(2).hours.at("00:00").do(mapping.getGateways)
    #schedule.every(1).second.do(mapping.getGateways)
    schedule.every(2).days.do(Utils.updateGeoIP)

    while True:
        schedule.run_pending()
        time.sleep(60)


th = threading.Thread(target=update)
th.start()

api.add_resource(Gateways, '/map/gateways')
api.add_resource(GatewaysCountries, '/map/gateways/countries')
api.add_resource(GatewaysOrg, '/map/gateways/orgs')
api.add_resource(GatewaysAS, '/map/gateways/asn')
api.add_resource(GatewaysContinent, '/map/gateways/continents')

if __name__ == '__main__':
    host = '0.0.0.0'

    app.run(debug=False, port='8080', host=host)
