import bz2
import s3fs
import os
import time

from concurrent.futures import ThreadPoolExecutor

from sats import satellites
from sats import satTypeGeneric

from . import dateCarrier 
from . import queryStringBuilder

from . import downloadManager

# init s3
fs = s3fs.S3FileSystem(anon=True)

def splitArray(arr, namnt):
    k, m = divmod(len(arr), namnt)
    return (arr[i*k+min(i, m):(i+1)*k+min(i+1, m)] for i in range(namnt))


def downloadS3BucketDay(saTime=dateCarrier.carrier(None, None, None, None, False), satellite=satellites.GENERIC, sector=satTypeGeneric.attrib.L1.FULL_DISK, datapathdir="../data", retainGz=True):

    attribs = satellite.getAttributes()

    # check if args were handed in correctly
    if satellite.IS_REAL == False:
        return 0

    gzPath = "{}/gz/{}/{}/".format(datapathdir[1], attribs.S3_SOURCE_PATH, saTime.getCompleteDateString()) 
    datPath = "{}/processed/{}/{}/".format(datapathdir[0], attribs.S3_SOURCE_PATH, saTime.getCompleteDateString())

    # lets create/check for a folder with the UNC name for the files
    if not os.path.exists(gzPath):
        os.makedirs(gzPath)

    if not os.path.exists(datPath):
        os.makedirs(datPath)

    # lets get the URI
    parentQueryURI = queryStringBuilder.buildCustomS3QueryDayOnly(saTime, satellite, sector)

    # get the dirs
    s3SubDirs = fs.ls(parentQueryURI.getQueryURI(), refresh=True)

    # internal method to wrap whats going on
    def threaddableDownload(file):
        downloadManager.singleDownloadExtract(gzPath, datPath, file)


    # lets start iterating over each container
    for s3dir in s3SubDirs:
        files = fs.ls(s3dir, refresh=True)

        # 160 files, 10 threads, 16 files per thread
        with ThreadPoolExecutor(max_workers=10) as executor:
            executor.map(threaddableDownload, files)