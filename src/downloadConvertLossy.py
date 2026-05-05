from satpy import Scene, find_files_and_readers, MultiScene, DataQuery
from satpy.composites.fill import BackgroundCompositor
from satpy.utils import debug_on
import dask

from remote import downloadManager
from sats import satellites
from remote import queryStringBuilder

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


def collectFromS3():
    himawariSat = satellites.HIMAWARI_9
    satribs = himawariSat.getAttributes()
    URI = queryStringBuilder.buildLatestS3QueryURI(sat=himawariSat, sector=satribs.L1.FULL_DISK)
    return downloadManager.getLatestDataFromS3(URI.getQueryURI(), saTime=URI, satellite=himawariSat)


def cleanDataDir():
    shutil.rmtree("../data/processed/")
    shutil.rmtree("../data/gz/")


# Main thread
while True:
    
    # download and extract the path of the data files
    path = os.path.dirname(collectFromS3()[0][0]) + "/"

    # configure dask with memory heap size before proceeding
    with dask.config.set({"array.chunk-size" : daskChunkSize}):
        
        print(f"Begin render of: {path}")

        ahi_dataset_reader = find_files_and_readers(base_dir=path, reader="ahi_hsd")
        dataset_scene = Scene(reader="ahi_hsd", filenames=ahi_dataset_reader, reader_kwargs={'mask_space': False})

        dataset_scene.load([active_template], generate=False)
        resampled_dataset_scene = dataset_scene.resample(dataset_scene.coarsest_area(), cachedir="../cache3", resampler="native")

        imageName = f"{active_template}.{datetime.datetime.now(timezone.utc)}.png"

        resampled_dataset_scene.save_datasets(dataset_id=active_template, filename=imageName, compute=True)

        # delete the processed data
        cleanDataDir()

        # move the image to completed folder
        shutil.move(imageName, "completed/")
        print(f"Rendered {imageName}")