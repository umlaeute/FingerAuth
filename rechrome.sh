#!/bin/sh

pkill -KILL chromium

chromium --use-fake-ui-for-media-stream --kiosk --app=$1 &
