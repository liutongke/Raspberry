#!/bin/bash
avconv -f video4linux2 -r 24 -i /dev/video0 -f flv rtmp://192.168.1.100/live/camera
