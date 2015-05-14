#!/bin/sh

xset s off
xset -dpms

cd "${0%/*}"
TIMESTAMP=$(date +%Y%m%d-%H%M)

loop() {
mkdir -p prophecies
while true; do
  echo "starting The Tech Oracle authenticator @ $(date)"
  ./FingerAuth.py 2>&1
  sleep 1
done
}

mkdir -p logs

export PYTHONUNBUFFERED=1
loop | tee "logs/Oracle-${TIMESTAMP}.log" 

