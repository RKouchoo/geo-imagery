from satpy import Scene, find_files_and_readers
from pathlib import WindowsPath

from remote import downloadManager
from sats import satellites
from remote import queryStringBuilder

from satpy.utils import debug_on
debug_on()


# https://github.com/pytroll/satpy/blob/main/satpy/etc/readers/ahi_hsd.yaml
# https://github.com/pytroll/satpy/blob/main/satpy/etc/composites/ahi.yaml

def SubDirPath (d):
    return [f for f in d.iterdir() if f.is_dir()]

def collectFromS3():
    himawariSat = satellites.HIMAWARI_9
    satribs = himawariSat.getAttributes()
    URI = queryStringBuilder.getLatestS3QueryAvaliable(sat=himawariSat, product=satribs.L1, sector=satribs.L1.FULL_DISK) # type: ignore
    downloadManager.getLatestDataFromS3(URI.getQueryURI(), saTime=URI, satellite=himawariSat) # type: ignore


collectFromS3()


subdirs = SubDirPath(WindowsPath(r'..\data\processed\noaa-himawari9'))

template = 'geo_color_background_with_low_clouds' # true_color

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



i = 0
for g in subdirs:

    i += 1
    f = find_files_and_readers(base_dir=g, reader='ahi_hsd')
    
    scenex = Scene(reader="ahi_hsd", filenames=f)
    scenex.load([template], generate=True)#, calibration="radiance")
    
    
    ns = scenex.resample(scenex.finest_area(), cache_dir="../cache2",  resampler='nearest') # nearest
    ns.save_dataset(dataset_id=template, writer="simple_image", filename=f"./himawari_{i}xyz4.png")
    


