import os 
import glob 

import subprocess
import shutil

geoDir = os.path.abspath("../../source_render/true_color_reproduction_night_ir")
clutDir = os.path.abspath("../../source_render/colorized_ir_clouds/")
clutDest = "proc"

geos = glob.glob(geoDir + "*.png")
weathers = glob.iglob(clutDir + '/*.png')

cluts = []


def doClutRender(path, source, dest):
	newpath = "{}\\{}\\{}".format(source, dest, os.path.basename(path))
	shutil.copyfile(path, newpath)
	clutArgs = "convert {} ( -clone 0 -colorspace CMYK -channel CMY -separate -evaluate-sequence add ) ( -clone 0,1 -alpha off -compose copyopacity -composite ) ( -clone 0 -fuzz 15%% +transparent white -blur 0x1.5 ) -delete 0,1 -compose over -composite {}".format(newpath, newpath)
	fixClutArgs = 'convert {}  -fuzz 20% -transparent "#9E0142" {}'.format(newpath, newpath)
	os.system(clutArgs)
	os.system(fixClutArgs)
	return newpath
	
	
def doImageMerge(geo, weather, result):
	args = "composite -compose over {} {} {}".format(weather, geo, result)
	return result
	


for weather in weathers:
	cluts.append(doClutRender(weather, clutDir, clutDest))
