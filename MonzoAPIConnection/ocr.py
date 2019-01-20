import http.client
import urllib.request
import urllib.parse
import urllib.error
import base64
import json
import time

# takes an image url and returns a list
# of text tokens contained in the image
def image_to_text(url):
    text = []

    # request headers
    headers = {
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': 'fbcc02faa1f04500b4275e49fba6bd62',
    }

    # request parameters
    params = urllib.parse.urlencode({
        # printed or handwritten
        'mode': 'Printed',
    })

    body = {"url": url}

    conn = http.client.HTTPSConnection('westcentralus.api.cognitive.microsoft.com')
    conn.request("POST", "/vision/v2.0/recognizeText?%s" % params, json.dumps(body), headers)
    response = conn.getresponse()
    x = response.getheader('Operation-Location')

    # wait for response
    time.sleep(5)

    # request parameters
    params2 = urllib.parse.urlencode({
        # take operation id
        # last part of url
        'operationId': x.split("/")[-1],
    })

    conn2 = http.client.HTTPSConnection("westcentralus.api.cognitive.microsoft.com")
    conn2.request("GET", "/vision/v2.0/textOperations/{operationId}?%s" % params2, "{body}", headers)
    response2 = conn2.getresponse()

    data2 = response2.read()
    z = json.loads(data2)

    # loop through each text token and append it to the list
    for item in z["recognitionResult"]["lines"]:
        text.append(str(item["text"]))

    conn2.close()
    conn.close()
    return text
