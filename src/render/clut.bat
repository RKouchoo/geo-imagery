echo off
REM arg %1 is the path to the file
echo %1
set out = %1_clut.png

convert %1 ( -clone 0 -colorspace CMYK -channel CMY -separate -evaluate-sequence add ) ( -clone 0,1 -alpha off -compose copyopacity -composite ) ( -clone 0 -fuzz 15%% +transparent white -blur 0x1.5 ) -delete 0,1 -compose over -composite %out%

REM remove the trailing edges of the image (colour #9E0142)
convert %out%  -fuzz 20%% -transparent "#9E0142" %out%