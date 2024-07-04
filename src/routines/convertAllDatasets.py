import glob
from satpy import Scene, find_files_and_readers
import os
from pathlib import WindowsPath
import warnings

#f = find_files_and_readers(base_dir="../data/processed/noaa-himawari9/202407021040/", reader='ahi_hsd')
#scene = Scene(filenames=f)

template = "true_color"

def SubDirPath (d):
    return [f for f in d.iterdir() if f.is_dir()]

subdirs = SubDirPath(WindowsPath(r"..\data\processed\noaa-himawari9"))
i = 0
for g in subdirs:
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=RuntimeWarning)
            
            i += 1
            f = find_files_and_readers(base_dir=g, reader='ahi_hsd')
            scenex = Scene(filenames=f)
            #print(scenex.available_composite_names())
            scenex.load([template], generate=False)
            ns = scenex.resample(scenex.coarsest_area(), cache_dir="./cache", resampler='native') #native nearest finestcoarsest_area()
            ns.save_dataset(template, filename=f"{i}.png")
            
    except Exception as e:
        print(e)
