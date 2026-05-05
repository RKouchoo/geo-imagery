#import glob
#from satpy import Scene, find_files_and_readers
from sats import satellites
from remote import queryStringBuilder

from remote import downloadManager

from remote import dateCarrier

import time


himawariSat = satellites.HIMAWARI_9
goesSat = satellites.GOES_18
goesAttribs = goesSat.getAttributes()
himAttribs = himawariSat.getAttributes()

#carrier = dateCarrier.carrier("2026", "02", "17", "0000", False)
#uri = queryStringBuilder.buildCustomS3Query(carrier, sat=himawariSat, sector=himAttribs.L1.FULL_DISK)

while True:
    uri = queryStringBuilder.buildLatestS3QueryURI(sat=himawariSat, sector=himAttribs.L1.FULL_DISK) # type: ignore
    downloadManager.getLatestDataFromS3(uri.getQueryURI(), saTime=uri, satellite=himawariSat)
    #print("Download finished, sleep 30 seconds before next download")
    #time.sleep(30)
    

#print(uri.getTime())

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