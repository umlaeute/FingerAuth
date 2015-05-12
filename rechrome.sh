#!/bin/sh

pkill -KILL chromium

chromium --kiosk --app=$1 &
