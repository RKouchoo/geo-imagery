from email.mime import image
from satpy import Scene, find_files_and_readers, MultiScene, DataQuery
from satpy.composites.fill import BackgroundCompositor
from satpy.utils import debug_on
import dask

from remote import downloadManager

import os
from pathlib import Path
import datetime
from datetime import date, timedelta, timezone
import shutil
import warnings
    
warnings.filterwarnings('ignore', 'Mean of empty slice', category=RuntimeWarning)
warnings.filterwarnings('ignore', 'invalid value encountered in divide', category=RuntimeWarning)

# https://github.com/pytroll/satpy/blob/main/satpy/etc/readers/ahi_hsd.yaml
# https://github.com/pytroll/satpy/blob/main/satpy/etc/composites/ahi.yaml

def SubDirPath (d):
    return [f for f in d.iterdir() if f.is_dir()]


opts =  ['airmass', 'ash', 'cloud_phase_distinction', 'cloud_phase_distinction_raw',
        'cloudtop', 'colorized_ir_clouds', 'convection', 'day_microphysics_ahi',
        'day_microphysics_eum', 'dust', 'fire_temperature', 'fire_temperature_39refl',
        'fire_temperature_awips', 'fire_temperature_eumetsat', 'fog', 'geo_color',
        'geo_color_background_with_low_clouds', 'geo_color_high_clouds', 'geo_color_low_clouds',
        'geo_color_night', 'hybrid_green', 'hybrid_green_nocorr', 'ir_cloud_day', 'mid_vapor',
        'natural_color', 'natural_color_nocorr', 'natural_color_raw', 'natural_color_raw_with_night_ir',
        'ndvi_hybrid_green', 'night_ir_alpha', 'night_ir_with_background', 'night_ir_with_background_hires',
        'night_microphysics', 'overview', 'overview_raw', 'reproduced_green', 'reproduced_green_uncorr',
        'rocket_plume_night', 'true_color', 'true_color_ndvi_green', 'true_color_nocorr', 'true_color_raw',
        'true_color_reproduction', 'true_color_reproduction_corr', 'true_color_reproduction_night_ir',
        'true_color_reproduction_uncorr', 'true_color_with_night_ir', 'true_color_with_night_ir_hires', 'water_vapors1', 'water_vapors2']

chann = ['B01', 'B02', 'B03', 'B04', 'B05', 'B06', 'B07', 'B08', 'B09', 'B10', 'B11', 'B12', 'B13', 'B14', 'B15', 'B16']


dask.config.set(**{'array.slicing.split_large_chunks': False})

#..\data\processed\noaa-himawari9\202602171430
subdirs = SubDirPath(Path(r'./data/processed/noaa-himawari9'))

active_template = 'true_color_reproduction' # true_color

render1 = "true_color_reproduction_uncorr" #colorized_ir_clouds true_color_reproduction_uncorr true_color_reproduction_corr

#print(f"{render1}.{datetime.datetime.timestamp(datetime.datetime.now())}.png")

for datadir in subdirs:
    with dask.config.set({"array.chunk-size" : "512MiB"}):
 
        imageName = f"{render1}.{str(datadir).strip("data/processed/noaa-himawari9/")}.png"

        print(imageName)

        ahi_dataset_reader = find_files_and_readers(base_dir=datadir, reader="ahi_hsd")
        dataset_scene = Scene(reader="ahi_hsd", filenames=ahi_dataset_reader, reader_kwargs={'mask_space': False})

        dataset_scene.load([render1], generate=False)
        resampled_dataset_scene = dataset_scene.resample(dataset_scene.coarsest_area(), cachedir="./rendercache", resampler="native")
       
        resampled_dataset_scene.save_datasets(dataset_id=render1, filename=imageName, compute=True)
        
        shutil.move(imageName, "completed/")
        #os.popen("./dataset_clut_merge.sh")
