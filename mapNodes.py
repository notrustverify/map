import utils
import requests
import traceback
import datetime
import utils
import time
from collections import Counter
from db import BaseModel

GATEWAYS = "/api/v1/gateways/"
ACCEPTED_VERSION = ["1.1.0", "1.1.1", "1.1.2", "1.1.3", "1.2.0"]


class MapNodes:

    def __init__(self):
        self.db = BaseModel()


    def getGateways(self):
        s = requests.Session()
        ipsPort = dict()
        selected = dict()
        print(f"{datetime.datetime.utcnow()} - update gateway set")
        countryCounter = {}
        countryCoordinates = []
        try:
            response = s.get(f"{utils.NYM_VALIDATOR_API_BASE}/{GATEWAYS}")

            if response.ok:
                gatewaySet = response.json()
                
                for gateway in gatewaySet:
                    if gateway.get('gateway') and gateway.get('gateway')['version'] in ACCEPTED_VERSION:
                        
                        ip = gateway['gateway']['host']
                        identityKey = gateway['gateway']['identity_key']

                        country = utils.Utils.getCountry(ip, s, "8bee822a8bf50b")

                        latitude = country['latitude']
                        longitude = country['longitude']
                        country = country['country']

                        countryCoordinates.append([latitude,longitude])

                        try:
                            countryCounter[country] = countryCounter[country]+1
                        except KeyError:
                            countryCounter[country] = 1
                        
                        self.db.insertGateway(identityKey, ip, latitude, longitude, country)
                        
            print(countryCounter)

            return countryCoordinates
        except (requests.RequestException,KeyError) as e:
            print(traceback.format_exc())
            exit(1)
