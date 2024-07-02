# Geo-Imagery

This is a tool to download the raw data uploaded to amazon S3  and create ultra high resolution images and geotiffs for research use. 


## Supported Satellites
- Japan: Himawari 9 
- USA: GOES 16 17 19
- South Korea: GeoKompsat 2a (GK-2A)


## Requirements

    numpy
    satpy
    glob
    s3fs
    bz2
    rioxarray

## Todo:

- Finish HDF file handling with correct timestamps
- Add HRIT file handling for non HDF satellites
- Add other satellites and required containers 
- Convert satellite type classes into DB's or JSON objects
- Create a UI 
