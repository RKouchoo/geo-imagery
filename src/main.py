import glob
from satpy import Scene, find_files_and_readers
from s3 import s3StringBuilder
from s3 import s3DownloadManager
from s3 import s3DateCarrier
from sats import satellites

# https://sites.google.com/view/raybellwaves/cheat-sheets/satpy
# https://noaa-himawari9.s3.amazonaws.com/index.html#AHI-L1b-FLDK/2024/06/25/0820/
# https://www.data.jma.go.jp/mscweb/en/himawari89/space_segment/spsg_ahi.html
# https://www.data.jma.go.jp/mscweb/en/himawari89/himawari_cast/himawari_cast.php


himawariSat = satellites.HIMAWARI_9
goesSat = satellites.GOES_18
goesAttribs = goesSat.getAttributes()
himAttribs = himawariSat.getAttributes()

#ags = s3DownloadManager.getLatestDataFromS3("noaa-himawari9/AHI-L1b-FLDK/2024/07/02/1040/", saTime=s3DateCarrier.carrier("2024", "07", "02", "1040", False), satellite=himawarisat)
#ags = s3DownloadManager.getLatestDataFromS3(uri[0], uri[1], satellite=himawarisat) # type: ignore

uri = s3StringBuilder.buildLatestS3QueryURI(sat=goesSat, sector=goesAttribs.L1.FULL_DISK) # type: ignore
#xs = s3StringBuilder.buildLatestS3QueryAvaliable(sat=himawariSat, product=himAttribs.L1, sector=himAttribs.L1.FULL_DISK)
#xv = s3StringBuilder.buildLatestS3QueryAvaliable(sat=goesSat, product=goesAttribs.L1, sector=goesAttribs.L1.FULL_DISK)

print(uri.getTime())

'''
cloud = "geocolor_high_clouds"


f = find_files_and_readers(base_dir="../data/processed/noaa-himawari9/202407021040/", reader='ahi_hsd')
scene = Scene(filenames=f)

failed = []
good = []
for comp in scene.available_composite_names():
    try:
        scenex = Scene(filenames=f)
        scenex.load([comp], generate=True)
        ns = scenex.resample(scenex.coarsest_area(), cache="/cache", resampler='native')
        ns.save_dataset(comp, filename=f"{comp}.png")
        good.append(comp)
    except:
        failed.append(comp)


'''