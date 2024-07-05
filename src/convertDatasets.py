import glob
from satpy import Scene, find_files_and_readers
import os
from pathlib import WindowsPath




#f = find_files_and_readers(base_dir="../data/processed/noaa-himawari9/202407021040/", reader='ahi_hsd')
#scene = Scene(filenames=f)

template = "true_color_nocorr"


def SubDirPath (d):
    return [f for f in d.iterdir() if f.is_dir()]

subdirs = SubDirPath(WindowsPath(r'..\data\processed\noaa-himawari9'))
i = 1
for g in subdirs:
    try:
        i += 1
        f = find_files_and_readers(base_dir=g, reader='ahi_hsd')
        scenex = Scene(filenames=f)
        #print(scenex.available_composite_names())
        scenex.load([template], generate=True)
        ns = scenex.resample(scenex.finest_area(), cache_dir="./cache", resampler='nearest') #native
        ns.save_dataset(template, filename=f"{i}.png")
    except Exception as e:
        print(e)
