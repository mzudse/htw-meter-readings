#!/bin/bash

cam_status=$(vcgencmd get_camera)
if [ $? -ne 0 ]; then
    echo "vcgencmd not available on your system. Make sure ur running this on ur raspberry"
    exit 1
fi

cam_status_grep=$(echo "$cam_status" | grep 'detected=1')

if [ -n "$cam_status_grep" ]; then
    if [ "$1" -eq "d" ]; then
        docker compose up -d
    else
        docker compose up
    fi
else
    echo "camera not detected"
    exit 1
fi