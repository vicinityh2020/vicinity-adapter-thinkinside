# INCANT: Thinkinside localisation and geofencing adapter for the VICINITY infrastructure

The INCANT adapter provides indoor localisation and geofencing support to the VICINITY infrastructure, allowing to gather position and status of tracked assets from the Vicinity platform.
The logical architecture on how to use the adapter is reported in the following Figure:

![architecture](https://raw.githubusercontent.com/vicinityh2020/vicinity-adapter-thinkinside/master/doc/incantn_arch.png)

In order to create an application scenario based on the INCANT adapters, the following pre-requisites should satisfied by a third-party:
1. The necessary RTLS infrastructure needs to be deployed in the monitored area. This will vary with the specific targeted scenario. The RTLS will be integrated through the ThinkIN platform which will facilitate application developers in the overall management of the localisation infrastructure.
2. A deployment is created on the ThinkIN platform. This includes the map of the environments where the objects will be moving and localised. All such environments should be monitored through the RTLS infrastructure.
3. A VICINITY Open Gateway should be installed, properly configured (https://github.com/vicinityh2020/vicinity-gateway-api)

Once this is performed, the following steps should be followed in order to utilise the adapters:
1. The adapter should be build (see instructions below)
2. The Adapter should be executed (see instructions below)
3. The Agent should be configured and executed.

## How ot build the adapter

The adapter is shipped with docker, for creating a new build image run:

docker build -t vicinity-thinkinside-adapter .

## How to run the adapter

docker run -p 9998:9000 -d vicinity-thinkinside-adapter


