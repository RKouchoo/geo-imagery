import bz2
import glob
#import satpy
#import s3fs

from s3 import s3StringBuilder
from s3 import s3DownloadManager
from sats import satellites

# https://sites.google.com/view/raybellwaves/cheat-sheets/satpy
# https://noaa-himawari9.s3.amazonaws.com/index.html#AHI-L1b-FLDK/2024/06/25/0820/
# https://www.data.jma.go.jp/mscweb/en/himawari89/space_segment/spsg_ahi.html
# https://www.data.jma.go.jp/mscweb/en/himawari89/himawari_cast/himawari_cast.php

himawarisat = satellites.HIMAWARI_9
attribs = himawarisat.getAttributes()

uri = s3StringBuilder.buildLatestS3QueryURI(sat=himawarisat, prod=attribs.L1.FULL_DISK, category=attribs.L1)
print(uri[0])
#s3DownloadManager.getLatestDataFromS3(uri[0], time=uri[1], satellite=himawarisat)

#print(uri)
#print(himawari(attribs.L1.ENCODER_TYPE))

# lets connect to s3 and grab all the data
#fs = s3fs.S3FileSystem(anon=True)
#files = fs.ls(s3Path) 


'''

def test():
    for fi in files:
        print(fi)
        fs.download(fi, f"glob/bz/{fi[-47:]}")


    bz = glob.glob("glob/bz/*.bz2")
    for zips in bz:
        zfile = bz2.BZ2File(zips)
        data = zfile.read()
        open(f"glob/decom/{zips[8:-4]}", "wb").write(data)


    filenamez = glob.glob("glob/decom/*.DAT")
    scene = satpy.Scene(filenames=filenamez, reader='ahi_hsd')

    ids = scene.all_dataset_ids()

    scene.load(["B05"])
    scene.show("B05")

    '''