import os
import time
import ipaddress
import traceback

import requests
import socket
from dotenv import load_dotenv

NYM_VALIDATOR_API_BASE = "https://validator.nymtech.net"
PREFERRED_IPINFO_API = "ipapi"

load_dotenv()


class Utils:
    ipInfoToken = os.getenv("IPINFO", None)

    @staticmethod
    def humanFormat(num, round_to=2):
        # From https://stackoverflow.com/questions/579310/formatting-long-numbers-as-strings-in-python
        magnitude = 0
        while abs(num) >= 1000:
            magnitude += 1
            num = round(num / 1000.0, round_to)
        return '{:.{}f} {}'.format(num, round_to, ['', 'K', 'M', 'G', 'T', 'P'][magnitude])

    @staticmethod
    def isIP(ip):
        try:
            ipaddress.ip_address(ip)
        except ValueError:
            return False

        return True

    @staticmethod
    def queryIPinfos(ip, s, token, api):
        if not (Utils.isIP(ip)):
            ip = Utils.getIP(ip)

        if api == "ipinfo":
            url = f'https://ipinfo.io/{ip}?token={token}'
        elif api == "ipapi":
            url = f'https://ipapi.co/{ip}/json/'
            time.sleep(1)

        try:
            response = s.get(url)
            if response.ok:
                return response.json()
            else:
                if response.json().get('reason') == "RateLimited":
                    return {'error': 'ratelimited'}

                if response.json().get('status') == '404':
                    f"Error {response.json()}"
                    return {}

                return {}
        except requests.Timeout as e:
            print(e)
            print(traceback.format_exc())

    @staticmethod
    def getIP(ip):
        return socket.gethostbyname(ip)

    @staticmethod
    def getCountry(ip, s, token, api="ipapi"):

        try:

            data = Utils.queryIPinfos(ip, s, token, api)
            if api == "ipinfo":
                return {'country': data['country'], 'city': data['city'], 'region': data['region'],
                        'org': data['org'],
                        'latitude': data['loc'].split(",")[0], 'longitude': data['loc'].split(",")[1]}

            elif api == "ipapi":

                # if ipapi is ratelimited, try to fallback to ipinfo
                if data.get('error') == "ratelimited" and token:
                    print("fallback on ipinfo")
                    data = Utils.queryIPinfos(ip, s, token, "ipinfo")
                    return {'country': data['country'], 'city': data['city'], 'region': data['region'],
                            'org': data['org'],
                            'latitude': data['loc'].split(",")[0], 'longitude': data['loc'].split(",")[1]}

                if data['latitude'] is None or data['longitude'] is None and token:
                    coordinatesIPinfo = Utils.queryIPinfos(ip, s, token, "ipinfo")
                    latitude = coordinatesIPinfo['loc'].split(",")[0]
                    longitude = coordinatesIPinfo['loc'].split(",")[1]
                    return {'country': data['country'], 'city': data['city'], 'region': data['region'],
                        'org': data['org'],
                        'asn': data['asn'], 'latitude': latitude, 'longitude': longitude}

                return {'country': data['country'], 'city': data['city'], 'region': data['region'],
                        'org': data['org'],
                        'asn': data['asn'], 'latitude': data['latitude'], 'longitude': data['longitude']}

        except (KeyError, ValueError) as e:
            print(f"Key/Value error {e} on getCountry, ip {ip}")
            return {}
