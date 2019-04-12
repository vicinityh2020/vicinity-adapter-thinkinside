import json
import random

import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

TAG_OID_SINGLE = 'thinkin-indoor-location-tag'
TAG_OID_SUMMARY = 'thinkin-indoor-location-summary'
LOCALISATION_URL = "http://localhost:8080/qpe/getTagPosition?version=2"
LOCALISATION_URL = "http://192.168.1.140:8080/qpe/getTagPosition?version=2"
LOCALISATION_URL2 = "http://localhost:8080/qpe/getTagPosition?version=2&maxAge=5000"
LOCALISATION_URL2 = "http://192.168.1.140:8080/qpe/getTagPosition?version=2&maxAge=5000"

TAG_LIST = []


@csrf_exempt
def location_tag(request, oid, pid):
    response = {
        'error_message': '',
        'property': pid,
        'value': -1
    }

    if oid != TAG_OID_SINGLE and oid != TAG_OID_SUMMARY:
        return JsonResponse(data=response, status=404)

    if request.method == 'GET' and oid == TAG_OID_SINGLE:
        try:
            response['value'] = get_tag_position(pid)
            return JsonResponse(data=response, status=200)
        except: 
            return JsonResponse(data=response, status=404)

    elif request.method == 'GET' and oid == TAG_OID_SUMMARY:
        response['value'] = get_tag_statistics()
        return JsonResponse(data=response, status=200)


    else:
        response['error_message'] = 'unsupported method'
        return JsonResponse(data=response, status=400)


def get_tag_statistics():
    r = requests.get(LOCALISATION_URL2)
    data = r.json()
    resp = {}

    resp['active_tags'] = len(data['tags'])
    resp['checkout_tags'] = len([1 for i in data['tags'] if computeZone(i) == "checkout"])
    resp['shopping_tags'] = len([1 for i in data['tags'] if computeZone(i) == "shopping"])
    
    for i in TAG_LIST:
        resp[i] = ""

    for i in data['tags']:
        resp[i['id']] = json.dumps({"ts": i['positionTS'], "x": i['position'][0], "y": i['position'][1], 'zone': computeZone(i)})

    return resp




def get_tag_position(tag_id):

    r = requests.get(LOCALISATION_URL)
    data = r.json()

    return [{'x': i['position'][0], 'y': i['position'][1], 'z': i['position'][2], 'ts': i['positionTS'], 'zone': computeZone(i)} for i in filter(lambda x: tag_id.startswith(x['id']), data['tags'])][0]


def computeZone(tag):
    x = float(tag['position'][0])
    y = float(tag['position'][1])



    if x > 67 and y > 20:
        return "checkout"
    if y > 11:
        return "shopping"

    return ""




def thing_descriptor(request):

    p_single = get_property_list()
    p_summary = get_property_summary()

    td = {
        "adapter-id": "thinkin-adapter-py",
        "thing-descriptions": [{
            "oid": TAG_OID_SINGLE,
            "name": "Realtime indoor location position",
            "type": "adapters:Thermometer",
            "properties": p_single,
            "actions": [],
            "events": []
        },
        {
            "oid": TAG_OID_SUMMARY,
            "name": "Realtime indoor location summary",
            "type": "adapters:Thermometer",
            "properties": p_summary,
            "actions": [],
            "events": []
        }
        ]
    }

    return JsonResponse(data=td, status=200)


def get_property_list():

    global TAG_LIST

    r = requests.get(LOCALISATION_URL)

    data = r.json()

    TAG_LIST = [ i['id'] for i in data['tags'] ]


    return [ {
                "pid": "%s-position" % i['id'],
                "monitors": "adapters:AmbientTemperature",
                "read_link": {
                    "href": "/objects/{oid}/properties/{pid}",#.format(oid=TAG_OID),
                    "output": 
                    {
                        "type": "object",
                        "field": [
                            {
                                "name": "x",
                                "schema": {
                                    "type": "integer"
                                    }
                                },
                            {
                                "name": "y",
                                "schema": {
                                    "type": "integer"
                                    }
                                },
                            {
                                "name": "timestamp",
                                "schema": {
                                    "type": "integer"
                                    }
                                },
                            {
                                "name": "zone",
                                "schema": {
                                    "type": "string"
                                    }
                                }
                            ]
                        }

                }
            } for i in data['tags']]


def get_property_summary():

    r = requests.get(LOCALISATION_URL)

    data = r.json()


    prop = {
                "pid": "summary",
                "monitors": "adapters:AmbientTemperature",
                "read_link": {
                    "href": "/objects/{oid}/properties/{pid}",#.format(oid=TAG_OID),
                    "output": 
                    {
                        "type": "object",
                        "field": [
                            {
                                "name": i['id'],
                                "schema": {
                                    "type": "string"
                                    }
                                } for i in data['tags']
                            ]
                        }
                    }
                }

    prop['read_link']['output']['field'].append({
                                "name": "active_tags",
                                "schema": {
                                    "type": "integer"
                                    }
                                })
    prop['read_link']['output']['field'].append({
                                "name": "checkout_tags",
                                "schema": {
                                    "type": "integer"
                                    }
                                })
    prop['read_link']['output']['field'].append({
                                "name": "shopping_tags",
                                "schema": {
                                    "type": "integer"
                                    }
                                })
    return prop
