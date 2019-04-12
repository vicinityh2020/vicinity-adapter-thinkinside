# VICINITY Thinkinside localisation and geofencing adapter

This adapter exposes the Thinkinside localisation and geofencing adapter to the Vicinity infrastructure, allowing to gather position and status of tracked assets from the Vicinity platform.

## How ot build the adapter

The adapter is shipped with docker, for creating a new build image run:

docker run -t vicinity-thinkinside-adapter .

## How to run the adapter

docker run -p 9998:9000 -d vicinity-thinkinside-adapter


