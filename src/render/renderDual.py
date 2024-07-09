import os 
import glob 

import subprocess

geoDir = ""
clutDir = ""

geos = glob.glob(geoDir + "*.png")
weathers = glob.glob(clutDir + "*.png")

for weather in weathers:
        weatherArgs = ["clut.bat", weather]
        subprocess.call(weatherArgs)

