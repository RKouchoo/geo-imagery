echo off

convert himawari_0000_storm.png ( -clone 0 -colorspace CMYK -channel CMY -separate -evaluate-sequence add ) ( -clone 0,1 -alpha off -compose copyopacity -composite ) ( -clone 0 -fuzz 15% +transparent white -blur 0x1.5 ) -delete 0,1 -compose over -composite storm.png

convert storm.png  -fuzz 20% -transparent "#9E0142" storm.png

composite -compose over storm.png himawari_0000_geo.png latest.png