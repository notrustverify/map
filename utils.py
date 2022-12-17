import datetime
import os
import shutil
import time
import ipaddress
import traceback
from pprint import pprint

import geoip2.database
import geoip2.errors
import requests
import socket
from dotenv import load_dotenv
import tarfile
from pathlib import Path

NYM_VALIDATOR_API_BASE = "https://validator.nymtech.net"
PREFERRED_IPINFO_API = "ipapi"

load_dotenv()


class Utils:
    IPINFO_TOKEN = os.getenv("IPINFO", None)
    GATEWAY_LAST_UPDATE_HOUR = int(os.getenv("GATEWAY_LAST_UPDATE_HOUR", 24))
    GEOIP_LICENSE_KEY = os.getenv("GEOIP_LICENSE_KEY", None)
    GEO_IP_EDITION = ['GeoLite2-City', 'GeoLite2-ASN', 'GeoLite2-Country']
    GEO_IP_FOLDER_DATA = f"./data/geoip2"

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
        except Exception:
            return False

        return True

    def getIP(ip):
        try:
            return socket.gethostbyname(ip)
        except Exception as e:
            print(f"error with {ip}, error {e}")
            return None
    @staticmethod
    def updateGeoIP():
        print(f"{datetime.datetime.utcnow()} - update geoip DB")

        for edition in Utils.GEO_IP_EDITION:
            try:
                filename = f"{Utils.GEO_IP_FOLDER_DATA}/{edition}"
                file = requests.get(
                    f'https://download.maxmind.com/app/geoip_download?edition_id={edition}&license_key={Utils.GEOIP_LICENSE_KEY}&suffix=tar.gz')
                if file.ok:
                    open(filename, 'wb').write(file.content)

                    mmdbFile = tarfile.open(filename)
                    mmdbFolder = mmdbFile.getnames()[0]
                    mmdbFile.extract(f"{mmdbFolder}/{edition}.mmdb", Utils.GEO_IP_FOLDER_DATA)
                    mmdbFile.close()
                    shutil.copy(f"{Utils.GEO_IP_FOLDER_DATA}/{mmdbFolder}/{edition}.mmdb", Utils.GEO_IP_FOLDER_DATA)
                    os.remove(f"{Utils.GEO_IP_FOLDER_DATA}/{edition}")
                    shutil.rmtree(f"{Utils.GEO_IP_FOLDER_DATA}/{mmdbFolder}", )
                else:
                    print(f"Error with geoip fetch: {file.content}")

            except Exception as e:
                print(f"Error with geoip update: {e}")


    # have to rewrite it at some time
    @staticmethod
    def localGeoIP(ip, withCountry=False):
        with geoip2.database.Reader('./data/geoip2/GeoLite2-City.mmdb') as reader:
            response = {"city": reader.city(ip)}

        with geoip2.database.Reader('./data/geoip2/GeoLite2-ASN.mmdb') as reader:
            response.update({"asn": reader.asn(ip)})

        if withCountry:
            with geoip2.database.Reader('./data/geoip2/GeoLite2-Country.mmdb') as reader:
                response.update({"country": reader.country(ip)})

        return response

    @staticmethod
    def queryIPinfos(ip, s, token=None, api=None):
        if not (Utils.isIP(ip)):
            ip = Utils.getIP(ip)

        if ip is None:
            return {}

        if api == "ipinfo":
            url = f'https://ipinfo.io/{ip}?token={token}'
        elif api == "ipapi":
            url = f'https://ipapi.co/{ip}/json/'
            time.sleep(1)
        elif api == "geoip2":
            return Utils.localGeoIP(ip)

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


    @staticmethod
    def getCountry(ip, s, token, api="ipapi"):
        try:

            data = Utils.queryIPinfos(ip, s, token, api)

            if data is None:
                return {}

            if api != "geoip2":
                try:
                    continent = Utils.queryIPinfos(ip, s, api="geoip2").get('city').continent.code
                    #pprint(Utils.queryIPinfos(ip, s, api="geoip2"))
                except (KeyError, geoip2.errors.GeoIP2Error,ValueError) as e:
                    continent = None
                    print(f"no continent found for {ip}, error {e}")

            if api == "ipinfo":
                return {'country': data['country'], 'city': data['city'], 'region': data['region'],
                        'org': data['org'],
                        'latitude': data['loc'].split(",")[0], 'longitude': data['loc'].split(",")[1],
                        'continent': continent}

            elif api == "ipapi":

                # if ipapi is ratelimited, try to fallback to ipinfo
                if data.get('error') == "ratelimited" and token:
                    print("fallback on ipinfo")
                    data = Utils.queryIPinfos(ip, s, token, "ipinfo")
                    return {'country': data['country'],
                            'org': data['org'],
                            'latitude': data['loc'].split(",")[0], 'longitude': data['loc'].split(",")[1],
                            'continent': continent}

                # ipapi doesn't always have the coordinates, try to use ipinfo if token
                if data['latitude'] is None or data['longitude'] is None and token:
                    coordinatesIPinfo = Utils.queryIPinfos(ip, s, token, "ipinfo")
                    latitude = coordinatesIPinfo['loc'].split(",")[0]
                    longitude = coordinatesIPinfo['loc'].split(",")[1]
                    return {'country': data['country'],
                            'org': data['org'],
                            'asn': data['asn'], 'latitude': latitude, 'longitude': longitude, 'continent': continent}

                return {'country': data['country'],
                        'org': data['org'],
                        'asn': data['asn'], 'latitude': data['latitude'], 'longitude': data['longitude'],
                        'continent': continent}

            elif api == "geoip2":
                return {'country': data['city'].country.iso_code,
                        'org': data['asn'].autonomous_system_organization,
                        'asn': data['asn'].autonomous_system_number, 'latitude': data['city'].location.latitude,
                        'longitude': data['city'].location.longitude, 'continent': data['city'].continent.code}

        except (KeyError, ValueError,IndexError) as e:
            print(f"Key/Value error {e} on getCountry, ip {ip}")
            return {}
