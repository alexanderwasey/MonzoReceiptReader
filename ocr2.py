import http.client, urllib.request, urllib.parse, urllib.error, base64, json, time

headers = {
    # Request headers
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': 'fbcc02faa1f04500b4275e49fba6bd62',
}

params = urllib.parse.urlencode({
    # Request parameters
    'mode': 'Printed',
})

body = {"url":"https://s3-eu-west-1.amazonaws.com/mondo-production-image-uploads/user_00009Vk182u7NXFlNmoBSz/ldPUTwxW7h6I4SKR5bHj-6f595092-3605-4937-88cc-e3c56e1cd5ed"}

try:
    conn = http.client.HTTPSConnection('westcentralus.api.cognitive.microsoft.com')
    conn.request("POST", "/vision/v2.0/recognizeText?%s" % params, "{body}", headers)
    response = conn.getresponse()
    data = response.read()
    print(data)
    x = response.getheader('Operation-Location')
    time.sleep(35)
    conn.close()
except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))

##body = {"url":"https://s3-eu-west-1.amazonaws.com/mondo-production-image-uploads/user_00009Vk182u7NXFlNmoBSz/ldPUTwxW7h6I4SKR5bHj-6f595092-3605-4937-88cc-e3c56e1cd5ed"}

##conn = http.client.HTTPSConnection('westcentralus.api.cognitive.microsoft.com')
##conn.request("POST", "/vision/v2.0/recognizeText?%s" % params, json.dumps(body) , headers)
##response = conn.getresponse()
    
##x = response.getheader('Operation-Location')
#print(json.dumps(response.getheaders()))
#params = urllib.parse.urlencode({response["Operation-Location"]})
##time.sleep(35)

params2 = urllib.parse.urlencode({
           # Request parameters
    'operationId': x.split("/")[-1],
})
conn2 = http.client.HTTPSConnection("westcentralus.api.cognitive.microsoft.com")
conn2.request("GET", "/vision/v2.0/textOperations/{operationId}?%s" % params2, "{body}", headers)  
response2 = conn2.getresponse()
conn2.close()
    
#z = analysis = response.json()
#x = response.getheader('Operation-Location')
#params = urllib.parse.urlencode({response["Operation-Location"]})

data2 = response2.read()

#conn.close()
#print(type(data2))
print(type("ABC")

conn.close()
