# Geo-Imagery

This is a tool to download the raw data uploaded to amazon S3 from geostationary satellites and create ultra high resolution image and/or geotiffs for research use.
Powered by satpy - I was not happy with how it functioned.


## Supported Satellites
- Japan: Himawari 8/9 (currently only one working)
- USA: GOES 16 17 19
- South Korea: GeoKompsat 2a (GK-2A)


## Requirements

    numpy
    satpy
    glob
    s3fs
    bz2
    rioxarray
    dask
    cv2

## System requirements (whats working well for me)
- 16 core CPU (modern 8 core minimum)
- 96GB RAM (<32GB you will need a lot of swap)
- 1TB SSD (24 hours of raw data is ~400GB, speed does matter here)

### Tested system specs:
- 96GB DDR4 
- AMD Threadripper 2920x
- 4TB SSD (4x1TB ZFS stripe)
- 1GBPS download speed
- Bonus: 16GB M5 Macbook Pro (~15-40GB of swap)


## Todo:

- Finish render routines
- Investigate NCI thredds further (currently down) 
- Finish GOES constellation implementation 
- Finish GK2A implementation 
- Investigate Russian satellite data feeds (Elektro L)
- Investigate Chinese satellite data feeds (Fengyun)