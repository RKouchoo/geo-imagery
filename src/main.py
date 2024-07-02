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


himawarisat = satellites.HIMAWARI_9
attribs = himawarisat.getAttributes()
#uri = s3StringBuilder.buildLatestS3QueryURI(sat=himawarisat, prod=attribs.L1.FULL_DISK) # type: ignore
#ags = s3DownloadManager.getLatestDataFromS3("noaa-himawari9/AHI-L1b-FLDK/2024/07/02/1040/", saTime=s3DateCarrier.carrier("2024", "07", "02", "1040", False), satellite=himawarisat)
#ags = s3DownloadManager.getLatestDataFromS3(uri[0], uri[1], satellite=himawarisat) # type: ignore

rgbname1 = "ir_cloud_day"
rgbname = "rocket_plume_night"
rgbname1 = "colorized_ir_clouds"
rgbname1 = "airmass"
rgbname1 = "fog"
rgbname1 = 'true_color_raw'
rgbname1 = "true_color_nocorr"
rgbname1 = 'true_color'
rgbname1 = 'natural_color_raw'

f = find_files_and_readers(base_dir="../data/processed/noaa-himawari9/202407021040/", reader='ahi_hsd')
scene = Scene(filenames=f)

failed = []
good = []
for comp in scene.available_composite_names():
    try:
        scene = Scene(filenames=f)
        scene.load([comp], generate=True)
        ns = scene.resample(scene.coarsest_area(), cache="/cache", resampler='native')
        ns.save_dataset(comp, filename=f"{comp}.png")
        good.append(comp)
    except:
        failed.append(comp)

print(failed, good)


#ns.save_datasets("true_color", filename="t.png")

#scene = scene.resample("native")
#print(scene.all_dataset_names())



#ids = scene.all_dataset_ids()
#
#print(scene.all_composite_ids())
