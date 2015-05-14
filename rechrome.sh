#!/bin/sh

#echo $1 && exit 0

pkill -KILL chromium

chromium --use-fake-ui-for-media-stream --kiosk --app=$1 &
