import logging
import traceback
from datetime import datetime, timedelta

from peewee import *

database = SqliteDatabase('./data/data.db', pragmas={'foreign_keys': 1})

logger = logging.getLogger('db')
logHandler = logging.getLogger('db')
logHandler.setLevel(logging.DEBUG)


class BaseModel(Model):
    def connect(self):
        try:
            database.connect()
        except Exception as e:
            print(traceback.format_exc())

    def close(self):
        try:
            database.close()
        except Exception as e:
            print(traceback.format_exc())

    def getPacketsLastUpdate(self):
        self.connect()

        try:
            with database.atomic():
                return None

        except IntegrityError as e:
            print(e)
            print(traceback.format_exc())
            return False
        except DoesNotExist as e:
            print(e)
            print(traceback.format_exc())
            return False
        finally:
            self.close()

    def insertGateway(self, identityKey, ip, latitude, longitude, country, org, asn):
        self.connect()
        try:
            with database.atomic():

                now = datetime.utcnow()

                GatewayCoordinate.insert(identityKey=identityKey, ip=ip, latitude=latitude, longitude=longitude,
                                         country=country, org=org, asn=asn, updated_on=now, created_on=now
                                         ).on_conflict(action="update", conflict_target=[GatewayCoordinate.identityKey],
                                                       update={'identityKey': identityKey, 'ip': ip,
                                                               'latitude': latitude, 'longitude': longitude,
                                                               'country': country, 'asn': asn, 'org': org,
                                                               'updated_on': datetime.utcnow()}).execute()

        except IntegrityError as e:
            print(e)
            print(traceback.format_exc())
            return False
        except DoesNotExist as e:
            print(e)
            print(traceback.format_exc())
            return False
        finally:
            self.close()

    def getLastUpdate(self):
        self.connect()

        try:
            with database.atomic():
                return list(GatewayCoordinate.select(GatewayCoordinate.updated_on).order_by(
                    GatewayCoordinate.updated_on.desc()).limit(1).dicts())[0]

        except IntegrityError as e:
            logHandler.exception(e)
            return False
        except DoesNotExist as e:
            logHandler.exception(e)
            return False
        finally:
            self.close()

    def getGatewayByTime(self):
        self.connect()
        try:
            with database.atomic():
                list()


        except IntegrityError as e:
            logHandler.exception(e)
            return False
        except DoesNotExist as e:
            logHandler.exception(e)
            return False
        finally:
            self.close()

    def getGateways(self, intervalHour=0):
        self.connect()
        try:
            with database.atomic():

                if intervalHour > 0:
                    nowDelta = datetime.utcnow() - timedelta(hours=intervalHour)
                    return list(GatewayCoordinate.select(GatewayCoordinate.identityKey, GatewayCoordinate.latitude,
                                                         GatewayCoordinate.longitude,
                                                         GatewayCoordinate.country, GatewayCoordinate.asn,
                                                         GatewayCoordinate.org, GatewayCoordinate.created_on,
                                                         GatewayCoordinate.updated_on).where(
                        GatewayCoordinate.updated_on >= nowDelta).dicts())

                return list(GatewayCoordinate.select(GatewayCoordinate.identityKey, GatewayCoordinate.latitude,
                                                     GatewayCoordinate.longitude,
                                                     GatewayCoordinate.country, GatewayCoordinate.asn,
                                                     GatewayCoordinate.org, GatewayCoordinate.created_on,
                                                     GatewayCoordinate.updated_on).dicts())

        except IntegrityError as e:
            logHandler.exception(e)
            return False
        except DoesNotExist as e:
            logHandler.exception(e)
            return False
        finally:
            self.close()

    def getGatewaysCountry(self, intervalHour=0):
        self.connect()
        try:
            with database.atomic():

                if intervalHour > 0:
                    nowDelta = datetime.utcnow() - timedelta(hours=intervalHour)

                    return list(GatewayCoordinate.select(
                        GatewayCoordinate.country, fn.COUNT(GatewayCoordinate.country).alias('occ')).where(
                        GatewayCoordinate.updated_on >= nowDelta).group_by(GatewayCoordinate.country).dicts())

                return list(GatewayCoordinate.select(
                    GatewayCoordinate.country, fn.COUNT(GatewayCoordinate.country).alias('occ')).group_by(
                    GatewayCoordinate.country).dicts())

        except IntegrityError as e:
            logHandler.exception(e)
            return False
        except DoesNotExist as e:
            logHandler.exception(e)
            return False
        finally:
            self.close()

    def getGatewaysAS(self, intervalHour=0):
        self.connect()
        try:
            with database.atomic():

                if intervalHour > 0:
                    nowDelta = datetime.utcnow() - timedelta(hours=intervalHour)

                    return list(GatewayCoordinate.select(
                        GatewayCoordinate.asn, fn.COUNT(GatewayCoordinate.asn).alias('occ')).where(
                        GatewayCoordinate.updated_on >= nowDelta).group_by(GatewayCoordinate.asn).dicts())

                return list(GatewayCoordinate.select(
                    GatewayCoordinate.asn, fn.COUNT(GatewayCoordinate.asn).alias('occ')).group_by(
                    GatewayCoordinate.asn).dicts())

        except IntegrityError as e:
            logHandler.exception(e)
            return False
        except DoesNotExist as e:
            logHandler.exception(e)
            return False
        finally:
            self.close()

    def getGatewaysOrg(self, intervalHour=0):
        self.connect()
        try:
            with database.atomic():

                if intervalHour > 0:
                    nowDelta = datetime.utcnow() - timedelta(hours=intervalHour)

                    return list(GatewayCoordinate.select(
                        GatewayCoordinate.org, fn.COUNT(GatewayCoordinate.org).alias('occ')).where(
                        GatewayCoordinate.updated_on >= nowDelta).group_by(GatewayCoordinate.org).dicts())

                return list(GatewayCoordinate.select(
                    GatewayCoordinate.org, fn.COUNT(GatewayCoordinate.org).alias('occ')).group_by(
                    GatewayCoordinate.org).dicts())

        except IntegrityError as e:
            logHandler.exception(e)
            return False
        except DoesNotExist as e:
            logHandler.exception(e)
            return False
        finally:
            self.close()


class GatewayCoordinate(BaseModel):
    class Meta:
        database = database
        db_table = 'gateway_coordinate'

    identityKey = TextField(unique=True)
    ip = TextField()
    latitude = FloatField(null=True)
    longitude = FloatField(null=True)
    country = TextField(null=True)
    org = TextField(null=True)
    asn = TextField(null=True)
    created_on = DateTimeField(default=datetime.utcnow)
    updated_on = DateTimeField(default=datetime.utcnow)


def create_tables():
    with database:
        database.create_tables([GatewayCoordinate])
