from typing import List

from . import s3DateUtil
from sats import satellites
from sats import satTypeGeneric


def buildLatestS3QueryURI(sat=satellites.GENERIC, prod=satTypeGeneric.attrib.L1.FULL_DISK):
    satribs = sat.getAttributes()
    goTime = s3DateUtil.getHimawariLatestDate(satribs.TIME_SCALE)
    URI = "{}/{}/{}/{}/{}/{}/".format(satribs.S3_SOURCE_PATH, sat(prod), goTime.getYear(), goTime.getMonth(), goTime.getDay(), goTime.getTime())
    return [URI, goTime]


def buildS3QueryURI(satellite, product, time):


    return 0

