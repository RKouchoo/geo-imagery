mv latest.png latest.png.old

mv natural_color*.png geo.png
mv colorized_ir_clouds*.png storm.png

convert storm.png \( -clone 0 -colorspace CMYK -channel CMY -separate -evaluate-sequence add \) \( -clone 0,1 -alpha off -compose copyopacity -composite \) \( -clone 0 -fuzz 15% +transparent white -blur 0x1.5 \) -delete 0,1 -compose over -composite storm.png

#mv latest.png %date:~10,4%%date:~7,2%%date:~4,2%_%time:~1,1%%time:~3,2%_previous.png

composite -compose over storm.png geo.png latest.png
rm storm.png 
rm geo.png