import datetime
import traceback
import backoff
import requests

import utils
from db import BaseModel
from utils import Utils

GATEWAYS = "/api/v1/gateways/"
MIXNODES = "/api/v1/mixnodes/"
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
                    if gateway.get('gateway') and (
                            gateway.get('gateway')['version'].split('.')[1] == ACCEPTED_VERSION[0].split('.')[1] or
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
                            # countryCounter[country] = countryCounter[country] + 1

                            # countryCounter[org] = countryCounter[org] + 1
                            # countryCounter[asn] = countryCounter[asn] + 1
                        except KeyError:
                            # countryCounter[country] =  1
                            countryCounter[continent] = 1
                            # countryCounter[org] = 1
                            # countryCounter[asn] = 1

                        if ipInfo:
                            self.db.insertGateway(identityKey, ip, latitude, longitude, country, org, asn, continent)

            print(countryCounter)

        except (requests.RequestException, KeyError,ConnectionError) as e:
            print(f"Error getting node info --> {e}")
            print(traceback.format_exc())


    @backoff.on_exception(utils.BACKOFF_ALGO, (requests.exceptions.ConnectionError, requests.exceptions.Timeout),
                          max_tries=utils.BACKOFF_MAX_TRIES)
    def getMixnodes(self):
        s = requests.Session()
        print(f"{datetime.datetime.utcnow()} - update mixnodes set")
        countryCounter = {}
        countryCoordinates = []
        try:
            response = s.get(f"{utils.NYM_VALIDATOR_API_BASE}/{MIXNODES}")

            if response.ok:
                mixnodeSet = response.json()

                for mixnode in mixnodeSet:

                    # filter the version
                    if mixnode.get('bond_information') and (
                            mixnode.get('bond_information')['mix_node']['version'].split('.')[1] ==
                            ACCEPTED_VERSION[0].split('.')[1] or
                            mixnode.get('bond_information')['mix_node']['version'].split('.')[1] ==
                            ACCEPTED_VERSION[1].split('.')[1]):

                        mixnodeData = mixnode['bond_information']['mix_node']
                        ip = mixnodeData['host']
                        identityKey = mixnodeData['identity_key']

                        api = "geoip2"
                        ipInfo = utils.Utils.getCountry(ip, s, Utils.IPINFO_TOKEN, api=api)
                        if ipInfo is {}:
                            continue

                        latitude = ipInfo.get('latitude')
                        longitude = ipInfo.get('longitude')
                        country = ipInfo.get('country')
                        org = ipInfo.get('org')
                        asn = ipInfo.get('asn')
                        continent = ipInfo.get('continent')

                        if api != "geoip2" and asn is None and org is not None:
                            asn = ipInfo.get('org').split(' ')

                            if len(asn) > 0 and asn[0].lower().startswith('as'):
                                asn = asn[0]
                            else:
                                asn = None

                        try:
                            countryCounter[continent] = countryCounter[continent] + 1
                            # countryCounter[country] = countryCounter[country] + 1

                            # countryCounter[org] = countryCounter[org] + 1
                            # countryCounter[asn] = countryCounter[asn] + 1
                        except KeyError:
                            # countryCounter[country] =  1
                            countryCounter[continent] = 1
                            # countryCounter[org] = 1
                            # countryCounter[asn] = 1

                        if ipInfo:
                            self.db.insertMixnode(identityKey, ip, latitude, longitude, country, org, asn, continent)

            print(countryCounter)

        except (requests.RequestException, KeyError,ConnectionError) as e:
            print(f"Error getting node info --> {e}")
            print(traceback.format_exc())
