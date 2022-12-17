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


    def insertGateway(self, identityKey, ip, latitude, longitude, country, org, asn,continent):
        self.connect()
        try:
            with database.atomic():

                now = datetime.utcnow()

                GatewayCoordinate.insert(identityKey=identityKey, ip=ip, latitude=latitude, longitude=longitude,
                                         country=country, org=org, asn=asn, continent=continent,updated_on=now, created_on=now
                                         ).on_conflict(action="update", conflict_target=[GatewayCoordinate.identityKey],
                                                       update={'identityKey': identityKey, 'ip': ip,
                                                               'latitude': latitude, 'longitude': longitude,
                                                               'country': country, 'asn': asn, 'org': org, 'continent': continent,
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
    def insertMixnode(self, identityKey, ip, latitude, longitude, country, org, asn,continent):
        self.connect()
        try:
            with database.atomic():

                now = datetime.utcnow()

                MixnodeCoordinate.insert(identityKey=identityKey, ip=ip, latitude=latitude, longitude=longitude,
                                         country=country, org=org, asn=asn, continent=continent,updated_on=now, created_on=now
                                         ).on_conflict(action="update", conflict_target=[MixnodeCoordinate.identityKey],
                                                       update={'identityKey': identityKey, 'ip': ip,
                                                               'latitude': latitude, 'longitude': longitude,
                                                               'country': country, 'asn': asn, 'org': org, 'continent': continent,
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
                                                         GatewayCoordinate.org, GatewayCoordinate.continent,GatewayCoordinate.created_on,
                                                         GatewayCoordinate.updated_on).where(
                        GatewayCoordinate.updated_on >= nowDelta).dicts())

                return list(GatewayCoordinate.select(GatewayCoordinate.identityKey, GatewayCoordinate.latitude,
                                                     GatewayCoordinate.longitude,
                                                     GatewayCoordinate.country, GatewayCoordinate.asn,
                                                     GatewayCoordinate.org, GatewayCoordinate.continent,GatewayCoordinate.created_on,
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

    def getGatewaysContinents(self, intervalHour=0):
        self.connect()
        try:
            with database.atomic():

                if intervalHour > 0:
                    nowDelta = datetime.utcnow() - timedelta(hours=intervalHour)

                    return list(GatewayCoordinate.select(
                        GatewayCoordinate.continent, fn.COUNT(GatewayCoordinate.continent).alias('occ')).where(
                        GatewayCoordinate.updated_on >= nowDelta).group_by(GatewayCoordinate.continent).dicts())

                return list(GatewayCoordinate.select(
                    GatewayCoordinate.continent, fn.COUNT(GatewayCoordinate.continent).alias('occ')).group_by(
                    GatewayCoordinate.continent).dicts())

        except IntegrityError as e:
            logHandler.exception(e)
            return False
        except DoesNotExist as e:
            logHandler.exception(e)
            return False
        finally:
            self.close()

    def getNumGateways(self, intervalHour=0):
        self.connect()
        try:
            with database.atomic():

                if intervalHour > 0:
                    nowDelta = datetime.utcnow() - timedelta(hours=intervalHour)

                    return GatewayCoordinate.select(
                        GatewayCoordinate.identityKey).count().where(
                        GatewayCoordinate.updated_on >= nowDelta).count()

                return GatewayCoordinate.select(
                        GatewayCoordinate.identityKey).count()

        except IntegrityError as e:
            logHandler.exception(e)
            return False
        except DoesNotExist as e:
            logHandler.exception(e)
            return False
        finally:
            self.close()

    def getMixnodes(self, intervalHour=0):
        self.connect()
        try:
            with database.atomic():

                if intervalHour > 0:
                    nowDelta = datetime.utcnow() - timedelta(hours=intervalHour)
                    return list(MixnodeCoordinate.select(MixnodeCoordinate.identityKey, MixnodeCoordinate.latitude,
                                                         MixnodeCoordinate.longitude,
                                                         MixnodeCoordinate.country, MixnodeCoordinate.asn,
                                                         MixnodeCoordinate.org, MixnodeCoordinate.continent,MixnodeCoordinate.created_on,
                                                         MixnodeCoordinate.updated_on).where(
                        MixnodeCoordinate.updated_on >= nowDelta).dicts())

                return list(MixnodeCoordinate.select(MixnodeCoordinate.identityKey, MixnodeCoordinate.latitude,
                                                     MixnodeCoordinate.longitude,
                                                     MixnodeCoordinate.country, MixnodeCoordinate.asn,
                                                     MixnodeCoordinate.org, MixnodeCoordinate.continent,MixnodeCoordinate.created_on,
                                                     MixnodeCoordinate.updated_on).dicts())

        except IntegrityError as e:
            logHandler.exception(e)
            return False
        except DoesNotExist as e:
            logHandler.exception(e)
            return False
        finally:
            self.close()


    def getMixnodesCountry(self, intervalHour=0):
        self.connect()
        try:
            with database.atomic():

                if intervalHour > 0:
                    nowDelta = datetime.utcnow() - timedelta(hours=intervalHour)

                    return list(MixnodeCoordinate.select(
                        MixnodeCoordinate.country, fn.COUNT(MixnodeCoordinate.country).alias('occ')).where(
                        MixnodeCoordinate.updated_on >= nowDelta).group_by(MixnodeCoordinate.country).dicts())

                return list(MixnodeCoordinate.select(
                    MixnodeCoordinate.country, fn.COUNT(MixnodeCoordinate.country).alias('occ')).group_by(
                    MixnodeCoordinate.country).dicts())

        except IntegrityError as e:
            logHandler.exception(e)
            return False
        except DoesNotExist as e:
            logHandler.exception(e)
            return False
        finally:
            self.close()
    def getMixnodesAS(self, intervalHour=0):
        self.connect()
        try:
            with database.atomic():

                if intervalHour > 0:
                    nowDelta = datetime.utcnow() - timedelta(hours=intervalHour)

                    return list(MixnodeCoordinate.select(
                        MixnodeCoordinate.asn, fn.COUNT(MixnodeCoordinate.asn).alias('occ')).where(
                        MixnodeCoordinate.updated_on >= nowDelta).group_by(MixnodeCoordinate.asn).dicts())

                return list(MixnodeCoordinate.select(
                    MixnodeCoordinate.asn, fn.COUNT(MixnodeCoordinate.asn).alias('occ')).group_by(
                    MixnodeCoordinate.asn).dicts())

        except IntegrityError as e:
            logHandler.exception(e)
            return False
        except DoesNotExist as e:
            logHandler.exception(e)
            return False
        finally:
            self.close()
    def getMixnodesOrg(self, intervalHour=0):
        self.connect()
        try:
            with database.atomic():

                if intervalHour > 0:
                    nowDelta = datetime.utcnow() - timedelta(hours=intervalHour)

                    return list(MixnodeCoordinate.select(
                        MixnodeCoordinate.org, fn.COUNT(MixnodeCoordinate.org).alias('occ')).where(
                        MixnodeCoordinate.updated_on >= nowDelta).group_by(MixnodeCoordinate.org).dicts())

                return list(MixnodeCoordinate.select(
                    MixnodeCoordinate.org, fn.COUNT(MixnodeCoordinate.org).alias('occ')).group_by(
                    MixnodeCoordinate.org).dicts())

        except IntegrityError as e:
            logHandler.exception(e)
            return False
        except DoesNotExist as e:
            logHandler.exception(e)
            return False
        finally:
            self.close()
    def getMixnodesContinents(self, intervalHour=0):
        self.connect()
        try:
            with database.atomic():

                if intervalHour > 0:
                    nowDelta = datetime.utcnow() - timedelta(hours=intervalHour)

                    return list(MixnodeCoordinate.select(
                        MixnodeCoordinate.continent, fn.COUNT(MixnodeCoordinate.continent).alias('occ')).where(
                        MixnodeCoordinate.updated_on >= nowDelta).group_by(MixnodeCoordinate.continent).dicts())

                return list(MixnodeCoordinate.select(
                    MixnodeCoordinate.continent, fn.COUNT(MixnodeCoordinate.continent).alias('occ')).group_by(
                    MixnodeCoordinate.continent).dicts())

        except IntegrityError as e:
            logHandler.exception(e)
            return False
        except DoesNotExist as e:
            logHandler.exception(e)
            return False
        finally:
            self.close()
    def getNumMixnode(self, intervalHour=0):
        self.connect()
        try:
            with database.atomic():

                if intervalHour > 0:
                    nowDelta = datetime.utcnow() - timedelta(hours=intervalHour)

                    return MixnodeCoordinate.select(
                        MixnodeCoordinate.identityKey).count().where(
                        MixnodeCoordinate.updated_on >= nowDelta).count()

                return MixnodeCoordinate.select(
                        MixnodeCoordinate.identityKey).count()

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
    continent = TextField(null=True)
    created_on = DateTimeField(default=datetime.utcnow)
    updated_on = DateTimeField(default=datetime.utcnow)


class MixnodeCoordinate(BaseModel):
    class Meta:
        database = database
        db_table = 'mixnode_coordinate'

    identityKey = TextField(unique=True)
    ip = TextField()
    latitude = FloatField(null=True)
    longitude = FloatField(null=True)
    country = TextField(null=True)
    org = TextField(null=True)
    asn = TextField(null=True)
    continent = TextField(null=True)
    created_on = DateTimeField(default=datetime.utcnow)
    updated_on = DateTimeField(default=datetime.utcnow)


def create_tables():
    with database:
        database.create_tables([GatewayCoordinate,MixnodeCoordinate])
