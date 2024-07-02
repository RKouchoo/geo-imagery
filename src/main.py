import bz2
import glob
#import satpy
#import s3fs

from s3 import s3StringBuilder
from s3 import s3DownloadManager
from s3 import s3DateCarrier
from sats import satellites

# https://sites.google.com/view/raybellwaves/cheat-sheets/satpy
# https://noaa-himawari9.s3.amazonaws.com/index.html#AHI-L1b-FLDK/2024/06/25/0820/
# https://www.data.jma.go.jp/mscweb/en/himawari89/space_segment/spsg_ahi.html
# https://www.data.jma.go.jp/mscweb/en/himawari89/himawari_cast/himawari_cast.php


himawarisat = satellites.HIMAWARI_9
attribs = himawarisat.getAttributes()
uri = s3StringBuilder.buildLatestS3QueryURI(sat=himawarisat, prod=attribs.L1.FULL_DISK) # type: ignore
#ags = s3DownloadManager.getLatestDataFromS3("noaa-himawari9/AHI-L1b-FLDK/2024/07/02/1040/", saTime=s3DateCarrier.carrier("2024", "07", "02", "1040"), satellite=himawarisat)
ags = s3DownloadManager.getLatestDataFromS3(uri[0], uri[1], satellite=himawarisat) # type: ignore

'''
    filenamez = glob.glob("glob/decom/*.DAT")
    scene = satpy.Scene(filenames=filenamez, reader='ahi_hsd')

    ids = scene.all_dataset_ids()

    scene.load(["B05"])
    scene.show("B05")

'''