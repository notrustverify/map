import utils
import requests
import traceback
import datetime
from utils import Utils
import time
from collections import Counter
from db import BaseModel

GATEWAYS = "/api/v1/gateways/"
ACCEPTED_VERSION = ["1.1.x", "1.2.x"]


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
                    # filter the version
                    if gateway.get('gateway') and (gateway.get('gateway')['version'].split('.')[1] == ACCEPTED_VERSION[0].split('.')[1] or
                                                   gateway.get('gateway')['version'].split('.')[1] == ACCEPTED_VERSION[1].split('.')[1]):

                        ip = gateway['gateway']['host']
                        identityKey = gateway['gateway']['identity_key']

                        ipInfo = utils.Utils.getCountry(ip, s, Utils.IPINFO_TOKEN, api="geoip2")

                        latitude = ipInfo.get('latitude')
                        longitude = ipInfo.get('longitude')
                        country = ipInfo.get('country')
                        org = ipInfo.get('org')
                        asn = ipInfo.get('asn')
                        continent = ipInfo.get('continent')

                        if asn is None and org is not None:
                            asn = ipInfo.get('org').split(' ')

                            if len(asn) > 0 and asn[0].lower().startswith('as'):
                                asn = asn[0]
                            else:
                                asn = None

                    try:
                        countryCounter[continent] = countryCounter[continent] + 1
                        #countryCounter[country] = countryCounter[country] + 1

                        # countryCounter[org] = countryCounter[org] + 1
                        # countryCounter[asn] = countryCounter[asn] + 1
                    except KeyError:
                        #countryCounter[country] =  1
                        countryCounter[continent] = 1
                        # countryCounter[org] = 1
                        # countryCounter[asn] = 1

                    if ipInfo:
                        self.db.insertGateway(identityKey, ip, latitude, longitude, country, org, asn, continent)

            print(countryCounter)

        except (requests.RequestException, KeyError) as e:
            print(traceback.format_exc())
            exit(1)
