from . import dateUtil
from . import dateCarrier
from sats import satellites
from sats import satTypeGeneric

import s3fs


# build the latest query based on time
# returns a carrier class
def buildLatestS3QueryURI(sat=satellites.GENERIC, sector=satTypeGeneric.attrib.L1.FULL_DISK, goTime=dateUtil.getLatestDateCarrier()):
    satribs = sat.getAttributes()
    goTime = dateUtil.getLatestDateCarrier()
    
    URI = "{}/{}/{}/".format(satribs.S3_SOURCE_PATH, sat(sector), goTime.getStdQueryString())
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
    for i in range(0, int(queDepth) - 1): # type: ignore
        s3Files = fs.ls(cwd, refresh=True)
        cwd = delimToLatest(s3Files)

    carrier = dateUtil.createCarrierFromURI(cwd)
    carrier.setIsGenerated(False)
    return carrier


def buildCustomS3Query(qcarrier=dateCarrier.carrier(None, None, None, None, True), sat=satellites.GENERIC, sector=satTypeGeneric.attrib.L1.FULL_DISK):
    satribs = sat.getAttributes()

    URI = "{}/{}/{}/".format(satribs.S3_SOURCE_PATH, sat(sector), qcarrier.getStdQueryString())
    if satribs.IS_DAY_NUM:
        URI = "{}/{}/{}/{}/{}/".format(satribs.S3_SOURCE_PATH, sat(sector), qcarrier.getYear(), qcarrier.getDayEpoch(), qcarrier.getHour())
        qcarrier.setQueryType(True)

    qcarrier.setQueryURI(URI)
    qcarrier.setIsGenerated(False)

    return qcarrier


# at the moment, I ony have himawari access to thredds
# will be adding goes support when I find it
def buildLatestTdQueryURI(offset=0):
    dd = dateUtil.getLatestDateCarrier(negativeOffset=offset)
    url = "https://thredds.nci.org.au/thredds/catalog/gc63/satellite-products/nrt/raw/himawari-ahi/fldk/latest/{}/catalog.xml".format(dd.getStdQueryString())
    
    dd.setQueryURI(url)

    return dd


# little helper to grab the last entry in an array always
def delimToLatest(array):
    return array[len(array) - 1]
    


