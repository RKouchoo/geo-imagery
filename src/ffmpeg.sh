ffmpeg -framerate 16 -pattern_type glob -i './completed/*.png' -vf "scale=3840:-2" -c:v libx264 -pix_fmt yuv420p output.mp4
