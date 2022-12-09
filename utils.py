import os
import time
import ipaddress
import requests
import socket
from dotenv import load_dotenv

NYM_VALIDATOR_API_BASE = "https://validator.nymtech.net"

load_dotenv()


class Utils:

    ipInfoToken=os.getenv("IPINFO")

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
    def queryIPinfos(ip, s, token=None):
        if not (Utils.isIP(ip)):
            ip = Utils.getIP(ip)

        if token is not None:
            url = f'https://ipinfo.io/{ip}?token={token}'
        else:
            url = f'https://ipapi.co/{ip}/json/'
            time.sleep(1)

        response = s.get(url)

        return response

    @staticmethod
    def getIP(ip):
        return socket.gethostbyname(ip)
        


    @staticmethod
    def getCountry(ip, s, token=None):

        try:
            sleepTime = 3
            retries = 1
            response = Utils.queryIPinfos(ip, s, token)

            if response.ok:
                data = response.json()
                # handle error for ipapi
                if not (token) and response.json().get('error'):
                    print(f"Error {response.json()}")
                    return {}

                if response.json().get('status') == '404':
                    f"Error {response.json()}"
                    pass
                    
                if token:
                    return {'country': data['country'], 'city': data['city'], 'region': data['region'], 'org': data['org'],
                            'latitude': data['loc'].split(",")[0], 'longitude': data['loc'].split(",")[1]}
                else:
                    return {'country': data['country'], 'city': data['city'], 'region': data['region'], 'org': data['org'], 'latitude': data['latitude'], 'longitude': data['longitude']}
            else:
                print(f"Data error {response.json()}")
                # try with ipapi
                response = Utils.queryIPinfos(ip, s)

                if response.ok:
                    data = response.json()
                    if response.json().get('error'):
                        print(f"Error {response.json()}")
                        return {}
                    return {'country': data['country'], 'city': data['city'], 'region': data['region'],
                            'org': data['org'], 'latitude': data['latitude'], 'longitude': data['longitude']}
                else:
                    return {}
        except requests.RequestException as e:
            print(e)
            return {}
