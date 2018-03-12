import sys
sys.path.insert(0, '../')

import config

PUT_HEADERS = {"Content-Type": "application/json",
        "Authorization": config.HTTP_BASIC_AUTH,
        "Cache-Control": "no-cache"
        }

def putDataToThing(thingName, propertyName, data):
    url = "http://{}/Thingworx/Things/{}/Properties/{}".format(config.THINGWORX_HOST, thingName, propertyName)
    querystring = {"appKey": config.APP_KEY}
    payload = {propertyName: data}
    respone = requests.request("PUT", url, data=payload, headers=PUT_HEADERS, params=querystring)
    return response.status_code
