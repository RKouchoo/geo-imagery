from satpy import Scene, find_files_and_readers, MultiScene, DataQuery
from satpy.composites.fill import BackgroundCompositor
from satpy.utils import debug_on
import dask

from remote import downloadManager
from sats import satellites
from remote import queryStringBuilder
from remote import dateCarrier

import os
from pathlib import Path
import datetime
from datetime import date, timedelta, timezone
import shutil
import warnings

    
warnings.filterwarnings('ignore', 'Mean of empty slice', category=RuntimeWarning)
warnings.filterwarnings('ignore', 'invalid value encountered in divide', category=RuntimeWarning)

dask.config.set(**{'array.slicing.split_large_chunks': False})
daskChunkSize = "512MiB"
active_template = 'true_color_reproduction_uncorr'

himawariSat = satellites.HIMAWARI_9
satribs = himawariSat.getAttributes()


def cleanDataDir():
    shutil.rmtree("../data/processed/")
    shutil.rmtree("../data/gz/")



def generateDayDownloadsURIList(year, month, day, sat, sec):
    URIList = []
    for i in range(0, 2400, 10):
        if i % 100 < 60:
            query = queryStringBuilder.buildCustomS3Query(dateCarrier.carrier(year, month, day, f"{i:04d}", False), sat, sec)
            URIList.append(query)

    return URIList
    


def collectFromS3(uriList, sat):
   results = []
   for uri in uriList:
    print(f"Downloading: {uri.getQueryURI()}")
    results.append(downloadManager.getLatestDataFromS3(uri.getQueryURI(), saTime=uri, satellite=sat))
        
   return results


# Main thread

dayURIList = generateDayDownloadsURIList("2026", "05", "04", himawariSat, satribs.L1.FULL_DISK)
downloadResults = collectFromS3(dayURIList, himawariSat)


for result in downloadResults:

    path = os.path.dirname(result[0][0]) + "/"
    
    with dask.config.set({"array.chunk-size" : daskChunkSize}):
        print(f"Begin render of: {path}")

        ahi_dataset_reader = find_files_and_readers(base_dir=path, reader="ahi_hsd")
        dataset_scene = Scene(reader="ahi_hsd", filenames=ahi_dataset_reader, reader_kwargs={'mask_space': False})

        dataset_scene.load([active_template], generate=False)
        resampled_dataset_scene = dataset_scene.resample(dataset_scene.coarsest_area(), cachedir="../cache3", resampler="native")

        imageName = f"{active_template}.{datetime.datetime.now(timezone.utc)}.png"

        resampled_dataset_scene.save_datasets(dataset_id=active_template, filename=imageName, compute=True)

        shutil.move(imageName, "dayCompleted/")
        print(f"Rendered {imageName}")

#cleanDataDir()