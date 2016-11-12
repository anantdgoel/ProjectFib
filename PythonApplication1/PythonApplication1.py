import http.client, urllib.request, urllib.parse, urllib.error, base64
import json
from pprint import pprint
from PythonApplication1 import http
headers = {
    # Request headers
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': '92e7b0d9a88a4a6495c5b40481cbe81e',
}

params = urllib.parse.urlencode({
    # Request parameters
    'visualFeatures': 'Adult',
    'language': 'en',
})
body = "{\"url\":\"http://www.gettyimages.ca/gi-resources/images/Homepage/Hero/UK/CMS_Creative_164657191_Kingfisher.jpg\"}"
try:
    conn = http.client.HTTPSConnection('api.projectoxford.ai')
    conn.request("POST", "/vision/v1.0/analyze?%s" % params, body, headers)
    response = conn.getresponse()
    data = response.read()
    data = json.loads(data.decode("utf-8"))
    print("isAdultContent")
    pprint(data['adult']['isAdultContent'])
    print("isRacyContent")
    pprint(data['adult']['isRacyContent'])
    #print(data)
    conn.close()
except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))