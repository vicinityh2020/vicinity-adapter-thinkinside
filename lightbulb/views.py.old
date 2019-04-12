import json

import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

LIGHT_OID = '5213bf96-c25a-40bf-891c-49cb84db2844'
OPENHAB_HOST = 'localhost'
OPENHAB_PORT = 8080

COLORS = {
    'green': '63,92,46',
    'red': '0,100,46',
    'yellow': '47,85,47',
    'blue': '244,100,47',
}

@csrf_exempt
def lightbulb_color(request, oid, pid):
    response = {
        'error_message': '',
        'property': 'color',
        'value': -1
    }

    # Temporary logic as this is a quick-fix adapter that will most likely be replaced by Philips Hue
    if oid != LIGHT_OID:
        return JsonResponse(data=response, status=404)

    if pid != 'color':
        return JsonResponse(data=response, status=404)

    if request.method == 'GET':
        # unfinished, not sure if this needs to be implemented
        return JsonResponse(data=response, status=200)

    elif request.method == 'PUT':
        body = json.loads(request.body)
        color = body['color']

        if color not in COLORS:
            response['error_message'] = "no color named {0}".format(color)
            return JsonResponse(data=response, status=400)
        requests.post(url='http://{HOST}:{PORT}/rest/items/LightColor'.format(HOST=OPENHAB_HOST, PORT=OPENHAB_PORT), data=COLORS[color])

        return JsonResponse(data=response, status=200)

    else:
        response['error_message'] = 'unsupported method'
        return JsonResponse(data=response, status=400)


def thing_descriptor(request):
    td = {
        "adapter-id": "openhab-ikea-lightbulb",
        "thing-descriptions": [{
            "oid": LIGHT_OID,
            "name": "IKEA light 1",
            "type": "core:Device",
            "properties": [{
                "pid": "color",
                "monitors": "adapters:DeviceStatus",
                "read_link": {
                    "href": "/devices/{oid}/properties/color".format(oid=LIGHT_OID),
                    "output": {
                        "type": "object",
                        "field": [{
                            "name": "property",
                            "schema": {
                                "type": "string"
                            }
                        }, {
                            "name": "value",
                            "schema": {
                                "type": "integer"
                            }
                        }]
                    }
                },
                "write_link": {
                    "href": "/devices/{oid}/properties/color".format(oid=LIGHT_OID),
                    "input": {
                        "type": "object",
                        "field": [{
                            "name": "value",
                            "schema": {
                                "type": "integer"
                            }
                        }, {
                            "name": "blink",
                            "schema": {
                                "type": "boolean"
                            }
                        }]
                    },
                    "output": {
                        "type": "object",
                        "field": [{
                            "name": "success",
                            "schema": {
                                "type": "boolean"
                            }
                        }]
                    }
                }
            }],
            "actions": [],
            "events": []
        }]
    }

    return JsonResponse(data=td, status=200)
