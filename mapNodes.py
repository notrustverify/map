import utils
import requests
import traceback
import datetime
from utils import Utils
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

                        ipInfo = utils.Utils.getCountry(ip, s, Utils.IPINFO_TOKEN,api="ipapi")

                        latitude = ipInfo.get('latitude')
                        longitude = ipInfo.get('longitude')
                        country = ipInfo.get('country')
                        org=ipInfo.get('org')
                        asn=ipInfo.get('asn')

                        if asn is None:
                            asn = ipInfo.get('org').split(' ')

                            if len(asn) > 0 and asn[0].lower().startswith('as'):
                                asn = asn[0]
                            else:
                                asn = None

                        countryCoordinates.append([latitude,longitude])

                        try:
                            countryCounter[country] = countryCounter[country]+1
                            #countryCounter[org] = countryCounter[org] + 1
                            #countryCounter[asn] = countryCounter[asn] + 1
                        except KeyError:
                            countryCounter[country] = 1
                            #countryCounter[org] = 1
                            #countryCounter[asn] = 1

                        if ipInfo:
                            self.db.insertGateway(identityKey, ip, latitude, longitude, country,org,asn)
                        
            print(countryCounter)

            return countryCoordinates
        except (requests.RequestException,KeyError) as e:
            print(traceback.format_exc())
            exit(1)
