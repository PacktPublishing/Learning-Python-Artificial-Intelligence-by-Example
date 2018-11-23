Dataset is available here:

https://drive.google.com/open?id=1oX7mKolh96gxj-EanR4XuMHkjJrEb6PS 



To create a movie from saved images, use the command:

`ffmpeg -framerate 10 -pattern_type glob -i '*.jpg' -c:v libx264 -r 10  -y -an out.mp4`
