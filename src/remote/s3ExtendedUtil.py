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


def downloadS3BucketDay(saTime=dateCarrier.carrier(None, None, None, None, False), satellite=satellites.GENERIC, parentQueryURI="", sector=satTypeGeneric.attrib.L1.FULL_DISK, datapathdir="./data", retainGz=True):
    attribs = satellite.getAttributes()

    # check if args were handed in correctly
    if satellite.IS_REAL == False:
        return 0


    if parentQueryURI != "":
        # good do nothing
        0 - 0 
    else:
        parentQueryURI = queryStringBuilder.buildCustomS3QueryDayOnly(saTime, satellite, sector)

    s3SubDirs = fs.ls(parentQueryURI.getQueryURI(), refresh=True)


    # lets start iterating over each container
    for s3dir in s3SubDirs:
        files = fs.ls(s3dir, refresh=True)

        if len(files) != attribs.RAW_DATA_COUNT:
            print(f"Download not ready yet: {s3dir}, skipping.")
            continue

        dates = [p for p in s3dir.split("/") if p.isdigit()]
        s3DateStamp = "".join(dates)

        gzPath = "{}/gz/{}/{}/".format(datapathdir, attribs.S3_SOURCE_PATH, s3DateStamp) 
        datPath = "{}/processed/{}/{}/".format(datapathdir, attribs.S3_SOURCE_PATH, s3DateStamp)

        # lets create/check for a folder with the UNC name for the files
        if not os.path.exists(gzPath):
            os.makedirs(gzPath)

        if not os.path.exists(datPath):
            os.makedirs(datPath)

        def threaddableDownload(file):
            if satellite.getAttributes().GZ_WRAPPED:
                downloadManager.singleDownloadExtract(gzPath, datPath, file, retainGz)
            else:
                downloadManager.doDownload(datPath, [file])


        # 160 files, 16 threads, 10 files per thread
        with ThreadPoolExecutor(max_workers=16) as executor:
            executor.map(threaddableDownload, files)

        print(f"Downloaded {s3dir} moving to next dataset")
        