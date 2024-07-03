from typing import List

from . import s3DateUtil
from . import s3DateCarrier
from sats import satellites
from sats import satTypeGeneric

import s3fs


# build the latest query based on time
# returns a carrier class
def buildLatestS3QueryURI(sat=satellites.GENERIC, sector=satTypeGeneric.attrib.L1.FULL_DISK):
    satribs = sat.getAttributes()
    goTime = s3DateUtil.getLatestDateCarrier(satribs.TIME_SCALE)
    
    URI = "{}/{}/{}/{}/{}/{}/".format(satribs.S3_SOURCE_PATH, sat(sector), goTime.getYear(), goTime.getMonth(), goTime.getDay(), goTime.getTime())
    if satribs.IS_DAY_NUM:
        URI = "{}/{}/{}/{}/{}/".format(satribs.S3_SOURCE_PATH, sat(sector), goTime.getYear(), goTime.getDayEpoch(), goTime.getHour())

    goTime.setQueryURI(URI)
    
    return goTime


# build the latest query based on whats avaliable in S3
# returns the query URI
# QUE_DEPTH must be configured correctly for the product!!!!!
def getLatestS3QueryAvaliable(sat=satellites.GENERIC, product=satTypeGeneric.attrib.L1, sector=satTypeGeneric.attrib.L1.FULL_DISK):
    satribs = sat.getAttributes()
    fs = s3fs.S3FileSystem(anon=True)
    
    baseQuery = "{}/{}".format(satribs.S3_SOURCE_PATH, sat(sector))
    cwd = delimToLatest(fs.ls(baseQuery, refresh=True))

    # we can do it the smart way but every s3 instance is different and would require spaghett
    queDepth = sat(product.QUE_DEPTH)
    for i in range(0, int(queDepth) - 1):
        s3Files = fs.ls(cwd, refresh=True)
        cwd = delimToLatest(s3Files)

    carrier = s3DateUtil.createCarrierFromURI(cwd)
    carrier.setIsGenerated(False)
    return carrier


def buildCustomS3Query(qcarrier=s3DateCarrier.carrier(None, None, None, None, True), sat=satellites.GENERIC, sector=satTypeGeneric.attrib.L1.FULL_DISK):
    satribs = sat.getAttributes()

    URI = "{}/{}/{}/{}/{}/{}/".format(satribs.S3_SOURCE_PATH, sat(sector), qcarrier.getYear(), qcarrier.getMonth(), qcarrier.getDay(), qcarrier.getTime())
    if satribs.IS_DAY_NUM:
        URI = "{}/{}/{}/{}/{}/".format(satribs.S3_SOURCE_PATH, sat(sector), qcarrier.getYear(), qcarrier.getDayEpoch(), qcarrier.getHour())
        qcarrier.setQueryType(True)

    qcarrier.setQueryURI(URI)
    qcarrier.setIsGenerated(False)

    return qcarrier



# little helper to grab the last entry in an array always
def delimToLatest(array):
    return array[len(array) - 1]
    


