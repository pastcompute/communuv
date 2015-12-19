#!/bin/sh

cd /home/pi/communuv

while true ; do

python communuv.py

killall alsaplayer

echo "Restarted!"

sleep 1

done
